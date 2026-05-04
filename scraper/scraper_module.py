from playwright.async_api import async_playwright

from database.db_posts import get_posts


class FBGroupScraper:
    def __init__(self, storage_path, scraper_init):
        self.scraper_init = scraper_init

        def load_seen_posts():
            rows = get_posts()
            seen = set()
            for row in rows:
                raw_post_text = row[1]  # second column in your query
                seen.add(raw_post_text)
            return seen

        self.storage_path = storage_path
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.seen_posts = load_seen_posts()

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False, slow_mo=200
        )
        self.context = await self.browser.new_context(storage_state=self.storage_path)
        self.page = await self.context.new_page()

    async def stop(self):
        await self.browser.close()
        await self.playwright.stop()

    async def goto_group(self, page_url):
        await self.page.goto(page_url, wait_until="load")
        await self.page.wait_for_timeout(5000)

    async def close_modals(self):
        modals = await self.page.query_selector_all('div[role="alertdialog"]')
        for modal in modals:
            try:
                btn = await modal.query_selector("button")
                if btn:
                    await btn.click()
                    await self.page.wait_for_timeout(500)
            except:
                pass

    async def scroll_and_collect(self, scrolls=12, step_fraction=0.6):
        new_posts = []

        for _ in range(scrolls):
            # Scroll by a fraction of the viewport height instead of jumping to bottom
            await self.page.evaluate(f"""
                window.scrollBy(0, window.innerHeight * {step_fraction});
            """)
            await self.page.wait_for_timeout(3000)
            await self.close_modals()

            posts = await self.page.query_selector_all(
                'div[data-ad-rendering-role="story_message"]'
            )
            for post in posts:
                text = (await post.inner_text()).strip()
                if text and text not in self.seen_posts:
                    self.seen_posts.add(text)
                    new_posts.append(text)

        new_posts.reverse()
        return new_posts

    async def gentle_refresh(self):
        await self.page.evaluate("window.scrollTo(0, 0)")
        await self.page.wait_for_timeout(2000)
        await self.page.reload(wait_until="load")
        await self.page.wait_for_timeout(5000)
