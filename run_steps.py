import json
from playwright.sync_api import sync_playwright

def run_steps(page, steps):
    for step in steps:
        action = step.get("action")
        selector = step.get("selector")
        value = step.get("value")
        milliseconds = step.get("milliseconds")
        
        if action == "goto":
            print(f"Going to {step['url']}")
            page.goto(step["url"])
        elif action == "click":
            print(f"Clicking {selector}")
            page.wait_for_selector(selector)
            page.click(selector)
        elif action == "fill":
            print(f"Filling {selector} with '{value}'")
            page.wait_for_selector(selector)
            page.fill(selector, value)
        elif action == "wait":
            print(f"Waiting for {milliseconds} ms")
            page.wait_for_timeout(milliseconds)
        elif action == "press":
            key = step.get("key")
            print(f"Pressing key '{key}'")
            page.keyboard.press(key)
        else:
            print(f"Unknown action: {action}")

def main():
    with open("steps.json", "r", encoding="utf-8") as f:
        steps = json.load(f)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        
        run_steps(page, steps)
        
        print("Test tamamlandı. Tarayıcı açık kalacak.")
        page.wait_for_timeout(15000)
        # context.close()
        # browser.close()

if __name__ == "__main__":
    main()
