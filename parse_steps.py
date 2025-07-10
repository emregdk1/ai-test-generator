import re

# Basit eşleşme ile selector bulan yardımcı fonksiyon
def find_selector(phrase, elements):
    phrase = phrase.lower().strip()
    for el in elements:
        texts = [el.get("text", ""), el.get("aria-label", ""), el.get("placeholder", ""), el.get("name", "")]
        for txt in texts:
            if txt and phrase in txt.lower():
                # Örnek: "text=Giriş Yap" veya input placeholder'ı ile eşleşirse input[placeholder='X']
                if el["tag"] in ["button", "a", "div", "span"]:
                    return f"text={txt.strip()}"
                elif el["tag"] == "input" and el["placeholder"]:
                    return f"input[placeholder='{el['placeholder']}']"
                elif el["tag"] == "input" and el["name"]:
                    return f"input[name='{el['name']}']"
    return None

# Doğal dil adımını Playwright step'ine çevir
def map_natural_step(step_text, elements):
    step_text = step_text.strip().lower()

    # 1. URL'e git
    match = re.search(r"(https?://[^\s]+)", step_text)
    if match:
        return {
            "action": "goto",
            "url": match.group(1),
            "description": step_text
        }

    # 2. Tıklama
    if "tıkla" in step_text:
        for word in ["buton", "link", "seçenek", "butona"]:
            if word in step_text:
                phrase = step_text.split(word)[-1].strip(" '\"")
                selector = find_selector(phrase, elements)
                return {
                    "action": "click",
                    "selector": selector,
                    "description": step_text
                }

    # 3. Yazı girme
    if "yaz" in step_text or "gir" in step_text:
        match = re.search(r"'([^']+)' (?:yaz|gir)", step_text)
        value = match.group(1) if match else "değer"
        field_match = re.search(r"inputuna|alana|kutusuna|kısmına|bölümüne", step_text)
        if field_match:
            label_match = re.search(r"'([^']+)' inputuna", step_text)
            label = label_match.group(1) if label_match else "input"
            selector = find_selector(label, elements)
            return {
                "action": "fill",
                "selector": selector,
                "value": value,
                "description": step_text
            }

    # 4. Bekleme
    if "bekle" in step_text:
        match = re.search(r"(\d+)\s*saniye", step_text)
        if match:
            ms = int(match.group(1)) * 1000
            return {
                "action": "wait",
                "milliseconds": ms,
                "description": step_text
            }

    return {
        "action": "unknown",
        "description": step_text
    }
