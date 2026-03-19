import asyncio

from scraper.post_pipeline import process_post
from scraper.scraper_module import FBGroupScraper


GROUP_URL = "https://web.facebook.com/groups/901727836168332"


async def run_agent(on_new_posts=None):
    scraper = FBGroupScraper(storage_path="fb_auth.json")

    await scraper.start()
    await scraper.goto_group(GROUP_URL)

    try:
        while True:
            print("[AGENT] Scanning for new posts...")

            await scraper.gentle_refresh()
            new_posts = await scraper.scroll_and_collect(scrolls=8)

            if new_posts:
                print(f"[AGENT] Found {len(new_posts)} new posts")
                for post in new_posts:
                    process_post(post)

                if on_new_posts:
                    on_new_posts()
            else:
                print("[AGENT] No new posts")

            await asyncio.sleep(300)  # 300 seconds

    finally:
        await scraper.stop()
