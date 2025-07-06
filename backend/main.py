from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from playwright.sync_api import sync_playwright
import asyncio
import re
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL ekle
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_playwright_steps(steps):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        def parse_step(step: str):
            s = step.strip().lower()

            if s.startswith("siteyi aç"):
                url = step.lower().replace("siteyi aç", "").strip()
                page.goto(url)

            elif "yazan elemana tıkla" in s:
                start = step.find("'") + 1
                end = step.find("'", start)
                text = step[start:end]
                page.wait_for_selector(f"text={text}", timeout=10000)
                page.click(f"text={text}")

            elif "'inputuna" in s and "yaz" in s:
                start = step.find("'") + 1
                end = step.find("'", start)
                placeholder = step[start:end]
                value_start = step.find(f"{placeholder}' inputuna") + len(f"{placeholder}' inputuna")
                value = step[value_start:].replace("yaz", "").strip()
                page.fill(f"input[placeholder='{placeholder}']", value)

            elif "saniye bekle" in s:
                match = re.search(r"(\d+)", step)
                if match:
                    saniye = int(match.group(1))
                    page.wait_for_timeout(saniye * 1000)

            else:
                print(f"Tanımlanamayan adım: {step}")

        results = []
        for step in steps:
            try:
                parse_step(step)
                # Ekran görüntüsünü sayfanın görünür kısmını alacak şekilde çekiyoruz
                screenshot_bytes = page.screenshot(full_page=False)
                screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

                results.append({
                    "step": step,
                    "status": "success",
                    "screenshot": screenshot_base64
                })
            except Exception as e:
                results.append({
                    "step": step,
                    "status": "fail",
                    "error": str(e)
                })

        browser.close()
        return results

@app.post("/run-test")
async def run_test(request: Request):
    data = await request.json()
    steps = data.get("steps", [])
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, run_playwright_steps, steps)
    return {"results": result}
