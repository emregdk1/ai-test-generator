from playwright.sync_api import sync_playwright
import json
from pathlib import Path

def analyze_page(url: str, output_path: str = "data/components.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_timeout(3000)  # Sayfa yüklenmesi için bekle

        # Sayfa üzerindeki form ve interaktif elementleri seç
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

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(components, f, indent=2, ensure_ascii=False)

        print(f"✅ {len(components)} bileşen analiz edilerek kaydedildi → {output_path}")
        browser.close()


if __name__ == "__main__":
    analyze_page("https://www.flypgs.com/")
