"""
HTML Parser for The Helper website.

This module provides functions to parse The Helper's HTML structure and extract
subject names, resources, URLs, and metadata.
"""

import re
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse, urlunparse, unquote

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError(
        "BeautifulSoup4 is required. Install it with: pip install beautifulsoup4"
    )


# Configure logging
logger = logging.getLogger(__name__)


def parse_semester_page(html: str) -> List[str]:
    """
    Extract subject names from semester page.

    The page shows "Choose Your Subject" with subject cards.
    Extracts subject names exactly as shown.

    Args:
        html: HTML content of the semester page

    Returns:
        List of subject names

    Example:
        >>> html = '<div class="subject-card">Data Structures</div>'
        >>> parse_semester_page(html)
        ['Data Structures']
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        subjects = []

        # Look for common subject card patterns
        # Try multiple selectors to handle different HTML structures
        selectors = [
            '.subject-card',
            '[class*="subject"]',
            'a[href*="/semesters/"]',
            '.card',
            '[data-subject]'
        ]

        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                # Extract text content
                text = element.get_text(strip=True)

                # Skip empty or very short texts
                if text and len(text) > 2:
                    # Avoid duplicates
                    if text not in subjects:
                        subjects.append(text)

        # If no subjects found with selectors, try finding links to subject pages
        if not subjects:
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/semesters/' in href and href.count('/') >= 3:
                    text = link.get_text(strip=True)
                    if text and text not in subjects:
                        subjects.append(text)

        logger.info(f"Extracted {len(subjects)} subjects from semester page")
        return subjects

    except Exception as e:
        logger.error(f"Error parsing semester page: {e}", exc_info=True)
        return []


def parse_subject_page(html: str) -> List[Dict[str, Any]]:
    """
    Extract all resources from subject page.

    Two sections: "Previous Year Questions" and "Study Notes And Other Resources"
    For each resource extracts: title, url, section
    Preserves original titles exactly.

    Args:
        html: HTML content of the subject page

    Returns:
        List of resource dictionaries with keys: title, url, section

    Example:
        >>> resources = parse_subject_page(html)
        >>> resources[0]
        {'title': 'PYQ Nov 2024', 'url': '/path/to/resource', 'section': 'Previous Year Questions'}
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        resources = []

        # Section mappings
        section_keywords = {
            'Previous Year Questions': ['previous', 'year', 'questions', 'pyq'],
            'Study Notes And Other Resources': ['study', 'notes', 'resources', 'other']
        }

        # Find all resource links
        for link in soup.find_all('a', href=True):
            href = link['href']
            title = link.get_text(strip=True)

            # Skip empty titles or navigation links
            if not title or len(title) < 3:
                continue

            # Skip common navigation items
            if title.lower() in ['home', 'back', 'menu', 'login', 'logout']:
                continue

            # Determine section by looking at parent elements or nearby headings
            section = _determine_section(link, soup, section_keywords)

            resource = {
                'title': title,
                'url': href,
                'section': section
            }

            resources.append(resource)

        # Also look for resource cards or divs
        for card in soup.select('[class*="resource"], [class*="card"]'):
            link = card.find('a', href=True)
            if link:
                title = card.get_text(strip=True) or link.get_text(strip=True)
                href = link['href']

                if title and href and len(title) >= 3:
                    section = _determine_section(card, soup, section_keywords)

                    # Avoid duplicates
                    if not any(r['url'] == href and r['title'] == title for r in resources):
                        resources.append({
                            'title': title,
                            'url': href,
                            'section': section
                        })

        logger.info(f"Extracted {len(resources)} resources from subject page")
        return resources

    except Exception as e:
        logger.error(f"Error parsing subject page: {e}", exc_info=True)
        return []


def _determine_section(element, soup, section_keywords: Dict[str, List[str]]) -> str:
    """
    Determine which section a resource belongs to by analyzing context.

    Args:
        element: The element to analyze
        soup: BeautifulSoup object
        section_keywords: Dictionary mapping section names to keywords

    Returns:
        Section name or 'Other'
    """
    # Look for headings before this element
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        heading_text = heading.get_text(strip=True).lower()

        for section_name, keywords in section_keywords.items():
            if any(keyword in heading_text for keyword in keywords):
                # Check if this element comes after this heading
                if heading.sourceline and element.sourceline:
                    if element.sourceline > heading.sourceline:
                        return section_name

    # Look at parent element classes or IDs
    parent = element.parent
    while parent:
        if parent.name in ['div', 'section', 'article']:
            classes = ' '.join(parent.get('class', [])).lower()
            elem_id = (parent.get('id') or '').lower()
            combined = classes + ' ' + elem_id

            for section_name, keywords in section_keywords.items():
                if any(keyword in combined for keyword in keywords):
                    return section_name
        parent = parent.parent

    return 'Other'


def extract_resource_urls(html: str) -> List[str]:
    """
    Extract resource page URLs from subject page.

    Handles URL patterns like: /semesters/3/data-structures-and-algorithm/pyq-nov-2024

    Args:
        html: HTML content of the subject page

    Returns:
        List of resource page URLs
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        urls = []

        # Pattern for resource URLs
        resource_pattern = re.compile(r'/semesters/\d+/[^/]+/.+')

        for link in soup.find_all('a', href=True):
            href = link['href']

            # Match resource URL pattern
            if resource_pattern.match(href):
                if href not in urls:
                    urls.append(href)

        logger.info(f"Extracted {len(urls)} resource URLs")
        return urls

    except Exception as e:
        logger.error(f"Error extracting resource URLs: {e}", exc_info=True)
        return []


def normalize_url(url: str, base_url: str = 'https://thehelper.vercel.app') -> str:
    """
    Normalize URLs for deduplication.

    - Remove fragments
    - Remove trailing slashes
    - Resolve relative URLs
    - Handle URL-encoded characters

    Args:
        url: URL to normalize
        base_url: Base URL for resolving relative URLs

    Returns:
        Normalized URL

    Example:
        >>> normalize_url('/path/to/resource#section')
        'https://thehelper.vercel.app/path/to/resource'
    """
    try:
        # Resolve relative URLs
        absolute_url = urljoin(base_url, url)

        # Parse URL
        parsed = urlparse(absolute_url)

        # Decode URL-encoded characters
        path = unquote(parsed.path)

        # Remove trailing slash
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]

        # Rebuild URL without fragment
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            parsed.query,
            ''  # No fragment
        ))

        return normalized

    except Exception as e:
        logger.error(f"Error normalizing URL '{url}': {e}")
        return url


def detect_google_drive_links(html: str) -> List[str]:
    """
    Find Google Drive links in the page.

    Extract file IDs from drive.google.com/file/d/... patterns
    Convert to direct download URLs.

    Args:
        html: HTML content

    Returns:
        List of Google Drive direct download URLs

    Example:
        >>> detect_google_drive_links(html)
        ['https://drive.google.com/uc?export=download&id=1ABC...']
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        drive_urls = []

        # Patterns for Google Drive URLs
        patterns = [
            re.compile(r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'),
            re.compile(r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)'),
            re.compile(r'docs\.google\.com/.*[?&]id=([a-zA-Z0-9_-]+)')
        ]

        # Search in links
        for link in soup.find_all('a', href=True):
            href = link['href']

            for pattern in patterns:
                match = pattern.search(href)
                if match:
                    file_id = match.group(1)
                    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'

                    if download_url not in drive_urls:
                        drive_urls.append(download_url)

        # Search in raw HTML text (in case URLs are not in href attributes)
        html_text = str(soup)
        for pattern in patterns:
            for match in pattern.finditer(html_text):
                file_id = match.group(1)
                download_url = f'https://drive.google.com/uc?export=download&id={file_id}'

                if download_url not in drive_urls:
                    drive_urls.append(download_url)

        logger.info(f"Detected {len(drive_urls)} Google Drive links")
        return drive_urls

    except Exception as e:
        logger.error(f"Error detecting Google Drive links: {e}", exc_info=True)
        return []


def extract_metadata_from_title(title: str) -> Dict[str, Any]:
    """
    Parse title to extract metadata.

    Extracts: year, month, exam_type hints

    Args:
        title: Resource title

    Returns:
        Dictionary with metadata: year, month, type_hint

    Examples:
        >>> extract_metadata_from_title("PYQ Nov 2024")
        {'year': 2024, 'month': 'Nov', 'type_hint': 'pyq'}

        >>> extract_metadata_from_title("CT Papers 2025")
        {'year': 2025, 'month': None, 'type_hint': 'ct'}
    """
    metadata = {
        'year': None,
        'month': None,
        'type_hint': None
    }

    try:
        title_lower = title.lower()

        # Extract year (4-digit number)
        year_match = re.search(r'\b(20\d{2})\b', title)
        if year_match:
            metadata['year'] = int(year_match.group(1))

        # Extract month (abbreviated or full)
        months = {
            'jan': 'Jan', 'january': 'Jan',
            'feb': 'Feb', 'february': 'Feb',
            'mar': 'Mar', 'march': 'Mar',
            'apr': 'Apr', 'april': 'Apr',
            'may': 'May',
            'jun': 'Jun', 'june': 'Jun',
            'jul': 'Jul', 'july': 'Jul',
            'aug': 'Aug', 'august': 'Aug',
            'sep': 'Sep', 'sept': 'Sep', 'september': 'Sep',
            'oct': 'Oct', 'october': 'Oct',
            'nov': 'Nov', 'november': 'Nov',
            'dec': 'Dec', 'december': 'Dec'
        }

        for month_key, month_abbr in months.items():
            if re.search(r'\b' + month_key + r'\b', title_lower):
                metadata['month'] = month_abbr
                break

        # Extract type hints
        type_hints = {
            'pyq': ['pyq', 'previous year', 'previous-year', 'past paper'],
            'ct': ['ct', 'class test', 'class-test'],
            'notes': ['notes', 'study notes', 'lecture notes'],
            'assignment': ['assignment', 'homework'],
            'tutorial': ['tutorial', 'tut'],
            'syllabus': ['syllabus'],
            'book': ['book', 'textbook', 'reference'],
            'solution': ['solution', 'answer', 'key']
        }

        for hint_type, keywords in type_hints.items():
            if any(keyword in title_lower for keyword in keywords):
                metadata['type_hint'] = hint_type
                break

        return metadata

    except Exception as e:
        logger.error(f"Error extracting metadata from title '{title}': {e}")
        return metadata


# Utility function for testing
def _test_parser():
    """Test the parser functions with sample HTML."""

    # Test semester page parsing
    semester_html = """
    <div class="container">
        <h1>Choose Your Subject</h1>
        <div class="subject-card">
            <a href="/semesters/3/data-structures">Data Structures and Algorithm</a>
        </div>
        <div class="subject-card">
            <a href="/semesters/3/database">Database Management Systems</a>
        </div>
    </div>
    """

    subjects = parse_semester_page(semester_html)
    print("Subjects:", subjects)

    # Test subject page parsing
    subject_html = """
    <div class="container">
        <h2>Previous Year Questions</h2>
        <a href="/semesters/3/data-structures/pyq-nov-2024">PYQ Nov 2024</a>
        <a href="/semesters/3/data-structures/pyq-may-2024">PYQ May 2024</a>

        <h2>Study Notes And Other Resources</h2>
        <a href="/semesters/3/data-structures/notes">Lecture Notes</a>
    </div>
    """

    resources = parse_subject_page(subject_html)
    print("Resources:", resources)

    # Test URL extraction
    urls = extract_resource_urls(subject_html)
    print("URLs:", urls)

    # Test URL normalization
    normalized = normalize_url("/path/to/resource#section")
    print("Normalized URL:", normalized)

    # Test Google Drive detection
    drive_html = """
    <a href="https://drive.google.com/file/d/1ABC123xyz/view">Download</a>
    """
    drive_links = detect_google_drive_links(drive_html)
    print("Drive links:", drive_links)

    # Test metadata extraction
    metadata = extract_metadata_from_title("PYQ Nov 2024")
    print("Metadata:", metadata)


if __name__ == '__main__':
    # Set up logging for testing
    logging.basicConfig(level=logging.INFO)
    _test_parser()
