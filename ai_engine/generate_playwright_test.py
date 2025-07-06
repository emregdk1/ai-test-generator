# ai_engine/generate_playwright_test.py

import json

def generate_playwright_test(json_path, output_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    steps = []
    for element in data:
        selector = element.get("id") or element.get("text") or element.get("tag")
        action = element.get("type", "click")

        if action == "interactive":
            steps.append(f'    await page.click(\'text="{selector}"\')')
        elif action == "input":
            steps.append(f'    await page.fill(\'#{selector}\', "test input")')
        # başka türler eklenebilir (dropdown, checkbox vs.)

    script = f"""
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://example.com")  # gerekirse burayı senaryoya göre dinamik yap
{chr(10).join(steps)}
        await page.wait_for_timeout(5000)  # sonuçları görmek için bekle
        await browser.close()

asyncio.run(run())
""".strip()

    with open(output_path, "w") as f:
        f.write(script)
