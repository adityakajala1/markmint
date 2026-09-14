import asyncio
import os
import sys

# Ensure our environment is set up
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from thehelpers.crawler import TheHelperCrawler
from thehelpers.downloader import ResourceDownloader
import thehelpers.downloader as dl_module

async def main():
    print("Starting full scrape of The Helper...")
    downloader = ResourceDownloader()
    
    async with TheHelperCrawler(headless=True) as crawler:
        print("Discovering semesters...")
        semesters = await crawler.discover_semesters()
        print(f"Found semesters: {semesters}")
        
        for sem in semesters:
            print(f"\n--- Scraping Semester {sem} ---")
            subjects = await crawler.discover_subjects(sem)
            print(f"Found subjects: {subjects}")
            
            for sub in subjects:
                print(f"  Scraping subject: {sub}")
                resources = await crawler.discover_resources(sem, sub)
                print(f"    Discovered {len(resources)} resources.")
                
                for res in resources:
                    print(f"      Resource: {res.title.encode('ascii', 'replace').decode('ascii')}")
                    try:
                        # 1. Ask crawler to find the actual download URL (e.g., GDrive link or direct PDF)
                        file_url = await crawler.get_resource_file_url(res.source_url)
                        if not file_url:
                            print(f"        [-] No direct file link found.")
                            continue
                            
                        # 2. Convert to the disjoint downloader format
                        # Provide a safe filename using the resource title
                        safe_filename = "".join([c if c.isalnum() else "_" for c in res.title]) + ".pdf"
                        
                        dl_resource = dl_module.DiscoveredResource(
                            url=file_url,
                            semester=str(sem),
                            subject=sub,
                            filename=safe_filename
                        )
                        
                        # 3. Download it
                        downloaded = await downloader.download(file_url, dl_resource)
                        print(f"        [+] Downloaded successfully: {downloaded.local_path} (Hash: {downloaded.sha256[:8]})")
                    except Exception as e:
                        print(f"        [!] Error downloading {res.title}: {e}")

if __name__ == "__main__":
    # Playwright requires the proactor event loop on Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())


