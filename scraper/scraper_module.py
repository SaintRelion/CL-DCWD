import re
from typing import Any, Dict, List, Optional

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

    async def scroll_and_collect(
        self, scrolls: int = 12, step_fraction: float = 0.6
    ) -> List[Dict[str, str]]:
        new_posts_this_round: List[Dict[str, str]] = []
        hit_boundary: bool = False

        for _ in range(scrolls):
            # If we already connected to our known timeline, stop scrolling!
            if hit_boundary:
                break

            await self.page.evaluate(f"""
                window.scrollBy(0, window.innerHeight * {step_fraction});
            """)
            await self.page.wait_for_timeout(3000)
            await self.close_modals()

            messages: List[Any] = await self.page.query_selector_all(
                'div[data-ad-rendering-role="story_message"]'
            )

            for msg in messages:
                # Extract text, name, and link in a single fast browser-side call
                post_data: Dict[str, Optional[str]] = await msg.evaluate("""
                    (element) => {
                        let text = element.innerText.trim();
                        let current = element.parentElement;
                        let name = "Unknown";
                        let link = null;

                        while (current && current !== document.body) {
                            let profileNode = current.querySelector('div[data-ad-rendering-role="profile_name"] [role="link"]');
                            if (profileNode) {
                                name = profileNode.innerText.trim();
                                link = profileNode.getAttribute('href');
                                break; // Found the author wrapper, stop climbing
                            }
                            current = current.parentElement;
                        }
                        return { text: text, name: name, link: link };
                    }
                """)

                text: str = post_data.get("text", "") or ""
                if not text:
                    continue

                if text in self.seen_posts:
                    hit_boundary = True
                    break  # Stop processing this DOM snapshot immediately
                else:
                    # Only add if it's new AND we haven't hit the boundary yet
                    already_added: bool = any(
                        p["text"] == text for p in new_posts_this_round
                    )

                    if not already_added:
                        raw_link: Optional[str] = post_data.get("link")
                        profile_link: str = "Unknown"

                        if raw_link:
                            match = re.search(r"/user/(\d+)", raw_link)
                            if match:
                                profile_link = f"https://www.facebook.com/profile.php?id={match.group(1)}"

                        new_posts_this_round.append(
                            {
                                "text": text,
                                "name": post_data.get("name", "Unknown") or "Unknown",
                                "link": profile_link,
                            }
                        )

        # Add to seen_posts tracking
        for post_dict in new_posts_this_round:
            self.seen_posts.add(post_dict["text"])

        new_posts_this_round.reverse()
        return new_posts_this_round

    async def gentle_refresh(self):
        await self.page.evaluate("window.scrollTo(0, 0)")
        await self.page.wait_for_timeout(2000)
        await self.page.reload(wait_until="load")
        await self.page.wait_for_timeout(5000)
