import json
from pathlib import Path

def build_playwright_selector(element):
    if element.get('id'):
        return f"#{element['id']}"
    if element.get('aria-label'):
        return f"[aria-label='{element['aria-label']}']"
    if element.get('name'):
        return f"[name='{element['name']}']"
    if element.get('placeholder'):
        return f"[placeholder='{element['placeholder']}']"
    if element.get('class'):
        classes = element['class'].split()
        return "." + ".".join(classes)
    if element.get('text'):
        text = element['text'].strip().replace('\n', ' ')
        return f'text="{text}"'
    return element.get('tag', '')

def add_selectors_to_components(input_path="data/components.json", output_path="data/components_with_selectors.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        components = json.load(f)

    for el in components:
        el['playwright_selector'] = build_playwright_selector(el)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(components, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(components)} bileşene selector eklendi → {output_path}")

if __name__ == "__main__":
    add_selectors_to_components()
