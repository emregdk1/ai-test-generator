import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://example.com")  # gerekirse burayı senaryoya göre dinamik yap

        await page.wait_for_timeout(5000)  # sonuçları görmek için bekle
        await browser.close()

asyncio.run(run())