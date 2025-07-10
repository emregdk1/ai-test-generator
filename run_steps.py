# run_steps.py
def run_steps(page, steps):
    results = []
    for step in steps:
        result = {"step": step.description if hasattr(step, 'description') else str(step)}

        try:
            if step.action == "goto":
                page.goto(step.url)

            elif step.action == "click":
                selector = resolve_selector(page, step.selector)
                page.click(selector)

            elif step.action == "fill":
                selector = resolve_selector(page, step.selector)
                page.fill(selector, step.value)

            elif step.action == "wait":
                page.wait_for_timeout(step.milliseconds)

            # Screenshot alma
            result["status"] = "success"
            result["screenshot"] = page.screenshot(full_page=True).decode("latin1")

        except Exception as e:
            result["status"] = "fail"
            result["error"] = str(e)
            result["screenshot"] = page.screenshot(full_page=True).decode("latin1")

        results.append(result)

    return results


def resolve_selector(page, selector):
    """
    Verilen selector çalışmazsa, alternatif benzerleri otomatik bulmaya çalışır.
    """
    try:
        page.wait_for_selector(selector, timeout=2000)
        return selector
    except:
        html = page.content()
        return suggest_alternative_selector(html, selector)


def suggest_alternative_selector(html, original_selector):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    keyword = extract_keyword_from_selector(original_selector)

    for tag in soup.find_all(True):
        if keyword.lower() in tag.get_text(strip=True).lower():
            if tag.name == "input":
                placeholder = tag.get("placeholder")
                if placeholder:
                    return f"input[placeholder='{placeholder}']"
            elif tag.name == "button" or tag.name == "a":
                return f"text={tag.get_text(strip=True)}"
    return original_selector


def extract_keyword_from_selector(selector):
    if "text=" in selector:
        return selector.split("text=")[-1].strip("'")
    elif "placeholder=" in selector:
        return selector.split("placeholder=")[-1].strip("'")
    return selector
