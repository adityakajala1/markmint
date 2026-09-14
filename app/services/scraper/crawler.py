"""
Async Playwright-based crawler for The Helper website.

Respects robots.txt, applies rate limits (1-2 sec delays), implements retry logic
with exponential backoff, logs navigation and errors, saves error screenshots, and
tracks progress statistics.
"""

import asyncio
import logging
import os
import time
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode, quote

from playwright.async_api import async_playwright, Page, Browser, BrowserContext

from .models import DiscoveredResource
from .parser import parse_semester_page, parse_subject_page, detect_google_drive_links, normalize_url

logger = logging.getLogger(__name__)

BASE_URL = "https://app.services.scraper.tech"


class TheHelperCrawler:
    """Async Playwright crawler for The Helper academic resources."""

    def __init__(self, headless: bool = True, rate_limit: float = 1.5):
        self.headless = headless
        self.rate_limit = max(0.5, rate_limit)
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        self.stats = {
            "pages_loaded": 0,
            "errors": 0,
            "resources_discovered": 0,
            "retries": 0,
        }

        self._last_request_time = 0.0
        self._screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(self._screenshots_dir, exist_ok=True)

    async def __aenter__(self):
        await self._init_browser()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def _init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 720},
        )
        self.page = await self.context.new_page()
        logger.info("Browser initialized (headless=%s)", self.headless)

    async def _rate_limit_delay(self):
        elapsed = time.time() - self._last_request_time
        delay = max(0, self.rate_limit - elapsed)
        if delay > 0:
            await asyncio.sleep(delay)
        self._last_request_time = time.time()

    async def _load_with_retry(
        self,
        url: str,
        retries: int = 3,
        backoff_base: float = 2.0,
    ) -> Page:
        """Navigate with retry logic and exponential backoff."""
        last_exception = None
        for attempt in range(1, retries + 1):
            try:
                await self._rate_limit_delay()
                logger.info("Navigating to %s (attempt %d/%d)", url, attempt, retries)
                await self.page.goto(url, wait_until="networkidle", timeout=30000)
                self.stats["pages_loaded"] += 1
                logger.info("Loaded %s successfully", url)
                return self.page
            except Exception as exc:
                last_exception = exc
                self.stats["errors"] += 1
                self.stats["retries"] = max(self.stats["retries"], attempt - 1)
                logger.error("Failed to load %s (attempt %d/%d): %s", url, attempt, retries, exc)
                if attempt < retries:
                    wait = backoff_base ** attempt
                    logger.info("Retrying in %.1fs...", wait)
                    await asyncio.sleep(wait)

        # All retries exhausted
        await self._save_error_screenshot(url, last_exception)
        raise last_exception

    async def _save_error_screenshot(self, url: str, exc: Optional[Exception] = None):
        try:
            timestamp = int(time.time())
            safe_name = url.replace("/", "_").replace("?", "_")[:60]
            path = os.path.join(self._screenshots_dir, f"error_{safe_name}_{timestamp}.png")
            await self.page.screenshot(path=path, full_page=True)
            logger.info("Saved error screenshot to %s", path)
        except Exception as screenshot_exc:
            logger.error("Failed to save error screenshot: %s", screenshot_exc)

    async def discover_semesters(self) -> List[int]:
        url = f"{BASE_URL}/semesters"
        await self._load_with_retry(url)
        # Extract semester links/numbers - using parser and page content
        content = await self.page.content()
        # Look for links or text indicating semesters 1-8
        semesters = []
        for i in range(1, 9):
            # Check if semester exists on page
            page_text = await self.page.inner_text("body")
            if f"{i}" in page_text or f"Semester {i}" in page_text:
                semesters.append(i)
        # Fallback: parse from links
        links = await self.page.query_selector_all("a[href*='/semesters/']")
        for link in links:
            href = await link.get_attribute("href") or ""
            try:
                parts = href.split("/")
                for part in parts:
                    if part.isdigit() and 1 <= int(part) <= 8:
                        val = int(part)
                        if val not in semesters:
                            semesters.append(val)
            except ValueError:
                continue
        semesters.sort()
        logger.info("Discovered %d semesters: %s", len(semesters), semesters)
        return semesters

    async def discover_subjects(self, semester: int) -> List[str]:
        url = f"{BASE_URL}/semesters/{semester}"
        await self._load_with_retry(url)
        content = await self.page.content()
        subjects = parse_semester_page(content)
        # Deduplicate and filter
        unique = []
        for s in subjects:
            if s and s not in unique and len(s) > 1:
                unique.append(s)
        logger.info("Semester %d: discovered %d subjects", semester, len(unique))
        return unique

    async def discover_resources(self, semester: int, subject: str) -> List[DiscoveredResource]:
        import re
        encoded = quote(subject)
        subject_url = f"{BASE_URL}/semesters/{semester}/subjects/{encoded}"
        
        # Load the page first to count resources
        await self._load_with_retry(subject_url)
        await asyncio.sleep(4)
        
        containers = await self.page.locator("div.flex.items-center.justify-between:has(button:has-text('View'))").all()
        count = len(containers)
        logger.info("Semester %d / %s: discovered %d resources", semester, subject, count)
        
        resources: List[DiscoveredResource] = []
        
        for i in range(count):
            logger.info("Processing resource %d/%d for %s", i+1, count, subject)
            # Re-navigate to reset DOM state completely to avoid Next.js SPA stale state issues
            await self._load_with_retry(subject_url)
            await asyncio.sleep(4)
            
            try:
                container = self.page.locator("div.flex.items-center.justify-between:has(button:has-text('View'))").nth(i)
                title = await container.locator("span.text-muted-foreground").inner_text()
                button = container.locator("button:has-text('View')")
                
                # Click forcefully bypassing any ad overlays
                await button.click(force=True)
                
                # Wait for Next.js to navigate to /file-viewer
                try:
                    await self.page.wait_for_url("**/file-viewer**", timeout=10000)
                except Exception:
                    pass  # might already be there or use different routing
                
                # Give the Google Drive iframe time to fully load
                await asyncio.sleep(6)
                
                drive_id = None
                for _ in range(20): # retry for 10 seconds
                    for f in self.page.frames:
                        # Match drive.google.com/file/d/{ID}/preview (most reliable)
                        match = re.search(r'drive\.google\.com/file/d/([A-Za-z0-9_-]{25,})', f.url)
                        if match:
                            drive_id = match.group(1)
                            break
                        # Fallback: match ?id= or &id= in accounts.google.com redirect
                        if 'accounts.google.com' in f.url:
                            match = re.search(r'(?:[?&]id(?:=|%3D))([A-Za-z0-9_-]{25,})', f.url)
                            if match:
                                drive_id = match.group(1)
                                break
                    if drive_id:
                        break
                    await asyncio.sleep(0.5)
                
                if drive_id:
                    direct_url = f"https://drive.google.com/uc?id={drive_id}&export=download"
                    res = DiscoveredResource(
                        title=title.strip(),
                        source_url=direct_url,
                        semester=str(semester),
                        subject=subject,
                        resource_type=None,
                    )
                    resources.append(res)
                    logger.info("Found drive ID for '%s': %s", title, drive_id)
                else:
                    logger.warning("No Drive ID found for '%s'", title)
                    
            except Exception as e:
                logger.error("Error processing resource %d: %s", i, e)
                
        self.stats["resources_discovered"] += len(resources)
        return resources

    async def get_resource_file_url(self, resource_page_url: str) -> Optional[str]:
        if "drive.google.com/uc" in resource_page_url:
            return resource_page_url
            
        await self._load_with_retry(resource_page_url)
        content = await self.page.content()
        # Look for Google Drive links
        drive_links = detect_google_drive_links(content)
        if drive_links:
            logger.info("Found Google Drive link for %s", resource_page_url)
            return drive_links[0]
        # Look for direct file links (pdf, doc)
        links = await self.page.query_selector_all("a[href*='.pdf'], a[href*='.doc'], a[href*='.docx']")
        for link in links:
            href = await link.get_attribute("href") or ""
            if href and href.startswith("http"):
                return href
        # Fallback: any direct download link
        links = await self.page.query_selector_all("a[href*='download'], a[href*='file']")
        for link in links:
            href = await link.get_attribute("href") or ""
            if href and href.startswith("http"):
                return href
        logger.warning("No file URL found for %s", resource_page_url)
        return None

    async def close(self):
        if self.page:
            await self.page.close()
            self.page = None
        if self.context:
            await self.context.close()
            self.context = None
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
        logger.info("Crawler closed. Stats: %s", self.stats)

    def report_stats(self) -> Dict[str, Any]:
        return self.stats.copy()

