import asyncio
import os
import sys
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.scraper.crawler import TheHelperCrawler
from backend.services.scraper.downloader import ResourceDownloader
import backend.services.scraper.downloader as dl_module

PROGRESS_FILE = "data/.download_cache/scrape_progress.json"


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": [], "failed": [], "stats": {"total_found": 0, "downloaded": 0, "skipped_no_id": 0, "errors": 0}}


def save_progress(progress):
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


async def main():
    import re
    from urllib.parse import quote

    print("=" * 60)
    print("  TheHelpers.tech Full Site Scraper")
    print("  Downloads ALL PDFs with Google Drive links")
    print("=" * 60)

    progress = load_progress()
    downloader = ResourceDownloader()

    async with TheHelperCrawler(headless=True) as crawler:
        print("\n[Phase 1] Discovering semesters...")
        semesters = await crawler.discover_semesters()
        print(f"  Found {len(semesters)} semesters: {semesters}")

        for sem in semesters:
            print(f"\n{'='*60}")
            print(f"  SEMESTER {sem}")
            print(f"{'='*60}")

            subjects = await crawler.discover_subjects(sem)
            print(f"  Found {len(subjects)} subjects")

            for sub_idx, sub in enumerate(subjects):
                sub_key = f"sem{sem}/{sub}"
                print(f"\n  [{sub_idx+1}/{len(subjects)}] {sub}")

                # Load subject page to count resources
                encoded = quote(sub)
                subject_url = f"https://app.services.scraper.tech/semesters/{sem}/subjects/{encoded}"

                try:
                    await crawler._load_with_retry(subject_url)
                    await asyncio.sleep(4)
                except Exception as e:
                    print(f"    [!] Failed to load subject page: {e}")
                    progress["stats"]["errors"] += 1
                    save_progress(progress)
                    continue

                containers = await crawler.page.locator("div.flex.items-center.justify-between:has(button:has-text('View'))").all()
                count = len(containers)
                print(f"    Found {count} resources")

                # Process each resource: discover Drive ID + download immediately
                for i in range(count):
                    # Re-navigate each time to reset SPA state
                    try:
                        await crawler._load_with_retry(subject_url)
                        await asyncio.sleep(4)
                    except Exception as e:
                        print(f"    [!] Navigation error: {e}")
                        continue

                    try:
                        container = crawler.page.locator("div.flex.items-center.justify-between:has(button:has-text('View'))").nth(i)
                        title = await container.locator("span.text-muted-foreground").inner_text()
                        title = title.strip()
                        safe_title = title.encode('ascii', 'replace').decode('ascii')
                        res_key = f"{sub_key}/{title}"

                        if res_key in progress["completed"]:
                            print(f"      [{i+1}/{count}] SKIP: {safe_title}")
                            continue

                        print(f"      [{i+1}/{count}] {safe_title} ... ", end="", flush=True)

                        # Click View button
                        button = container.locator("button:has-text('View')")
                        await button.click(force=True)

                        # Wait for /file-viewer navigation
                        try:
                            await crawler.page.wait_for_url("**/file-viewer**", timeout=10000)
                        except Exception:
                            pass

                        await asyncio.sleep(6)

                        # Extract Drive ID from frames
                        drive_id = None
                        for _ in range(20):
                            for f in crawler.page.frames:
                                match = re.search(r'drive\.google\.com/file/d/([A-Za-z0-9_-]{25,})', f.url)
                                if match:
                                    drive_id = match.group(1)
                                    break
                                if 'accounts.google.com' in f.url:
                                    match = re.search(r'(?:[?&]id(?:=|%3D))([A-Za-z0-9_-]{25,})', f.url)
                                    if match:
                                        drive_id = match.group(1)
                                        break
                            if drive_id:
                                break
                            await asyncio.sleep(0.5)

                        if not drive_id:
                            print("no Drive link")
                            progress["stats"]["skipped_no_id"] += 1
                            save_progress(progress)
                            continue

                        # Download immediately
                        progress["stats"]["total_found"] += 1
                        file_url = f"https://drive.google.com/uc?id={drive_id}&export=download"
                        safe_filename = "".join([c if c.isalnum() or c in "._- " else "_" for c in title]).strip() + ".pdf"

                        dl_resource = dl_module.DiscoveredResource(
                            url=file_url,
                            semester=str(sem),
                            subject=sub,
                            filename=safe_filename
                        )

                        downloaded = await downloader.download(file_url, dl_resource)
                        print(f"OK ({downloaded.size // 1024} KB)")

                        progress["completed"].append(res_key)
                        progress["stats"]["downloaded"] += 1
                        save_progress(progress)

                    except Exception as e:
                        print(f"ERROR: {e}")
                        progress["stats"]["errors"] += 1
                        save_progress(progress)

    stats = progress["stats"]
    print(f"\n{'='*60}")
    print(f"  SCRAPE COMPLETE")
    print(f"{'='*60}")
    print(f"  Total resources found:   {stats['total_found']}")
    print(f"  Successfully downloaded: {stats['downloaded']}")
    print(f"  Skipped (no Drive ID):   {stats['skipped_no_id']}")
    print(f"  Errors:                  {stats['errors']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
