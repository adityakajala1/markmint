import aiohttp
import sqlite3
import hashlib
import os
import logging
from urllib.parse import urlparse, parse_qs
from typing import Optional
import asyncio
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscoveredResource:
    """Represents a discovered resource to be downloaded."""
    def __init__(self, url: str, semester: str, subject: str, filename: str):
        self.url = url
        self.semester = semester
        self.subject = subject
        self.filename = filename

class DownloadedResource:
    """Represents a downloaded resource."""
    def __init__(self, local_path: str, sha256: str, size: int):
        self.local_path = local_path
        self.sha256 = sha256
        self.size = size

class ResourceDownloader:
    def __init__(self, cache_dir: str = "data/.download_cache", storage_dir: str = "data/raw"):
        """
        Initialize the ResourceDownloader.

        Args:
            cache_dir: Directory for SQLite cache database
            storage_dir: Base directory for storing downloaded files
        """
        self.cache_dir = cache_dir
        self.storage_dir = storage_dir
        self.max_file_size = 50 * 1024 * 1024  # 50MB

        # Create directories if they don't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.storage_dir, exist_ok=True)

        # Initialize SQLite cache
        self.db_path = os.path.join(self.cache_dir, "downloads.db")
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database for download tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_normalized TEXT UNIQUE,
                sha256 TEXT UNIQUE,
                local_path TEXT,
                download_timestamp REAL,
                file_size INTEGER,
                source_metadata TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def normalize_url(self, url: str) -> str:
        """
        Normalize URL for consistent hashing.

        Args:
            url: URL to normalize

        Returns:
            Normalized URL string
        """
        parsed = urlparse(url)
        # Remove fragment and normalize path
        normalized = parsed._replace(fragment="", params="", query="").geturl()
        # Sort query parameters if any
        if parsed.query:
            query_parts = parse_qs(parsed.query, keep_blank_values=True)
            sorted_query = "&".join([f"{k}={'&'.join(sorted(v))}" for k, v in sorted(query_parts.items())])
            normalized = parsed._replace(query=sorted_query, fragment="").geturl()
        return normalized

    def convert_google_drive_url(self, url: str) -> str:
        """
        Convert Google Drive sharing URL to direct download URL.

        Args:
            url: Google Drive sharing URL

        Returns:
            Direct download URL
        """
        parsed = urlparse(url)
        if 'drive.google.com' in parsed.netloc:
            # Handle file/d/{id}/view format
            if '/file/d/' in parsed.path:
                file_id = parsed.path.split('/file/d/')[1].split('/')[0]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            # Handle open?id={id} format
            elif 'open' in parsed.path and 'id' in parse_qs(parsed.query):
                file_id = parse_qs(parsed.query)['id'][0]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            # Handle uc?export=download&id={id} (already direct)
            elif 'uc' in parsed.path and 'export=download' in parsed.query:
                return url
        return url

    async def download_with_retry(self, url: str, max_retries: int = 3) -> bytes:
        """
        Download file with retry mechanism and exponential backoff.

        Args:
            url: URL to download from
            max_retries: Maximum number of retry attempts

        Returns:
            Downloaded file content as bytes

        Raises:
            Exception: If all retry attempts fail
        """
        for attempt in range(max_retries):
            try:
                timeout = aiohttp.ClientTimeout(total=120)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        content_type = response.headers.get('Content-Type', '')
                        
                        # Check content length if available
                        content_length = response.headers.get('Content-Length')
                        if content_length and int(content_length) > self.max_file_size:
                            raise ValueError(f"File size {content_length} exceeds limit of {self.max_file_size} bytes")

                        # Read in chunks to handle large files and enforce size limit
                        chunks = []
                        total_size = 0
                        async for chunk in response.content.iter_chunked(8192):
                            total_size += len(chunk)
                            if total_size > self.max_file_size:
                                raise ValueError(f"Downloaded file size {total_size} exceeds limit of {self.max_file_size} bytes")
                            chunks.append(chunk)

                        data = b''.join(chunks)
                        
                        # Google Drive returns an HTML confirmation page for large files
                        # Check if we got HTML instead of a real file
                        if b'text/html' in content_type.encode() or (data[:100].strip().startswith(b'<!') and b'confirm' in data[:5000]):
                            import re
                            # Try to find the confirm URL  
                            html_text = data.decode('utf-8', errors='ignore')
                            # Look for form action with confirm token
                            confirm_match = re.search(r'href="(/uc\?export=download[^"]*confirm=[^"]*)"', html_text)
                            if not confirm_match:
                                confirm_match = re.search(r'action="([^"]*)"', html_text)
                            if confirm_match:
                                confirm_url = confirm_match.group(1).replace('&amp;', '&')
                                if confirm_url.startswith('/'):
                                    confirm_url = f"https://drive.google.com{confirm_url}"
                                logger.info(f"Following Google Drive confirmation redirect...")
                                async with session.get(confirm_url) as confirm_resp:
                                    confirm_resp.raise_for_status()
                                    chunks2 = []
                                    total2 = 0
                                    async for chunk in confirm_resp.content.iter_chunked(8192):
                                        total2 += len(chunk)
                                        if total2 > self.max_file_size:
                                            raise ValueError(f"File too large: {total2}")
                                        chunks2.append(chunk)
                                    return b''.join(chunks2)
                        
                        return data
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < max_retries - 1:
                    # Exponential backoff: 2^attempt seconds
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All {max_retries} attempts failed for {url}")
                    raise

    def calculate_sha256(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of a file in chunks.

        Args:
            file_path: Path to the file

        Returns:
            SHA-256 hash as hexadecimal string
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def check_duplicate(self, sha256: str) -> Optional[str]:
        """
        Check if a file with the given SHA-256 hash already exists in cache.

        Args:
            sha256: SHA-256 hash to check

        Returns:
            Existing file path if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT local_path FROM downloads WHERE sha256 = ?", (sha256,))
        result = cursor.fetchone()
        conn.close()

        if result:
            logger.info(f"Duplicate found for hash {sha256}: {result[0]}")
            return result[0]
        return None

    async def download(self, url: str, resource: DiscoveredResource) -> DownloadedResource:
        """
        Download a file from URL with deduplication.

        Args:
            url: URL to download from
            resource: DiscoveredResource containing metadata

        Returns:
            DownloadedResource with local path and hash
        """
        # Normalize URL for consistent caching
        normalized_url = self.normalize_url(url)

        # Convert Google Drive URLs if needed
        download_url = self.convert_google_drive_url(normalized_url)
        logger.info(f"Downloading from: {download_url}")

        # Download the file content
        content = await self.download_with_retry(download_url)

        # Calculate SHA-256 hash
        # We'll write to a temporary file to calculate hash
        temp_dir = os.path.join(self.cache_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, f"temp_{hashlib.md5(download_url.encode()).hexdigest()}")

        with open(temp_file, "wb") as f:
            f.write(content)

        file_hash = self.calculate_sha256(temp_file)
        file_size = len(content)

        # Check for duplicates
        existing_path = self.check_duplicate(file_hash)
        if existing_path:
            logger.info(f"Duplicate file found. Using existing: {existing_path}")
            # Clean up temp file
            os.remove(temp_file)
            # Return reference to existing file
            return DownloadedResource(
                local_path=existing_path,
                sha256=file_hash,
                size=file_size
            )

        # No duplicate found, save to storage directory
        # Create semester/subject directory structure
        storage_path = os.path.join(
            self.storage_dir,
            resource.semester,
            resource.subject,
            resource.filename
        )
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)

        # Move temp file to final location
        os.replace(temp_file, storage_path)
        logger.info(f"Saved file to: {storage_path}")

        # Record in cache database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO downloads
            (url_normalized, sha256, local_path, download_timestamp, file_size, source_metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            normalized_url,
            file_hash,
            storage_path,
            time.time(),
            file_size,
            f"semester:{resource.semester},subject:{resource.subject}"
        ))
        conn.commit()
        conn.close()

        return DownloadedResource(
            local_path=storage_path,
            sha256=file_hash,
            size=file_size
        )
