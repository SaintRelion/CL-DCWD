from playwright.async_api import async_playwright
import asyncio


async def save_auth():
    async with async_playwright() as p:
        # Note: Using 'chrome' channel is good for avoiding bot detection
        browser = await p.chromium.launch(headless=False, channel="chrome")
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.facebook.com")

        print("\n--- ACTION REQUIRED ---")
        print("1. Log in to Facebook manually in the opened browser.")
        print("2. Wait until you see your News Feed.")
        print("3. Return to this terminal and press Enter to save session.")

        # This allows the Playwright loop to stay active while waiting
        await asyncio.get_event_loop().run_in_executor(None, input)

        # Save the state
        await context.storage_state(path="fb_auth.json")
        print("Success! Auth state saved to fb_auth.json")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(save_auth())
