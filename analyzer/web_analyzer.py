from playwright.sync_api import sync_playwright

def analyze_page(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_timeout(3000)  # Sayfa yüklenmesi için bekle

        elements = page.query_selector_all("button, input, label, select, textarea")

        components = []
        for el in elements:
            try:
                tag = el.evaluate("e => e.tagName.toLowerCase()")
                text = el.inner_text().strip()
                id_attr = el.get_attribute("id") or ""
                name_attr = el.get_attribute("name") or ""
                aria_label = el.get_attribute("aria-label") or ""
                placeholder = el.get_attribute("placeholder") or ""
                class_attr = el.get_attribute("class") or ""
                type_attr = el.get_attribute("type") or ""

                components.append({
                    "tag": tag,
                    "text": text,
                    "id": id_attr,
                    "name": name_attr,
                    "aria-label": aria_label,
                    "placeholder": placeholder,
                    "class": class_attr,
                    "type": type_attr
                })
            except Exception as e:
                print(f"⚠️ Element alınamadı: {e}")

        browser.close()
        return components  # ← JSON dosyasına yazmak yerine liste olarak dön
