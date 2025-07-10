from playwright.async_api import async_playwright

async def analyze_page_elements(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        elements = await page.query_selector_all("*")
        dom_summary = []

        for el in elements:
            try:
                tag = await el.evaluate("e => e.tagName.toLowerCase()")
                text = await el.inner_text()
                aria_label = await el.get_attribute("aria-label")
                placeholder = await el.get_attribute("placeholder")
                name = await el.get_attribute("name")
                id_ = await el.get_attribute("id")
                class_ = await el.get_attribute("class")

                dom_summary.append({
                    "tag": tag,
                    "text": text.strip(),
                    "aria-label": aria_label,
                    "placeholder": placeholder,
                    "name": name,
                    "id": id_,
                    "class": class_,
                })
            except:
                continue

        await browser.close()
        return dom_summary
