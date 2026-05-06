import asyncio
from datetime import datetime

from scraper.post_pipeline import process_post
from scraper.scraper_module import FBGroupScraper

GROUP_URL = "https://web.facebook.com/groups/867214026016354"


async def run_agent(on_new_posts=None):
    scraper_init = datetime.now()
    scraper = FBGroupScraper(storage_path="fb_auth.json", scraper_init=scraper_init)

    await scraper.start()
    await scraper.goto_group(GROUP_URL)

    try:
        while True:
            print("[AGENT] Scanning for new posts...")

            await scraper.gentle_refresh()
            new_posts = await scraper.scroll_and_collect(scrolls=14)

            if new_posts:
                print(f"[AGENT] Found {len(new_posts)} new posts")

                # Format the logging to show the new locked-together data
                for idx, post in enumerate(new_posts, 1):
                    print(f"--- New Post {idx} ---")
                    print(f"Author: {post.get('name')}")
                    print(f"Link:   {post.get('link')}")
                    print(f"Text:   {post.get('text')}")
                    print("-" * 30)

                process_post(new_posts, scraper_init)

                if on_new_posts:
                    on_new_posts()
            else:
                print("[AGENT] No new posts")

            await asyncio.sleep(200)  # 200 seconds

    finally:
        await scraper.stop()


# asyncio.run(run_agent())
