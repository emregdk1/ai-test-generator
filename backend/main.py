from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import base64
import asyncio
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# ✅ CORS düzgün yapılandırıldı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dilersen sadece "http://localhost:5500" yazabilirsin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestRequest(BaseModel):
    steps: List[str]

@app.post("/run-test")
async def run_test(request: TestRequest):
    steps = request.steps
    results = []

    def run_playwright_steps(steps):
        logging.info("Test başladı...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            logging.info("Tarayıcı başlatıldı...")

            for step in steps:
                logging.info(f"Adım işleniyor: {step}")
                try:
                    if step.startswith("Siteyi aç"):
                        url = step.split(" ")[2]
                        page.goto(url)
                    elif "inputuna" in step and "yaz" in step:
                        value = step.split("yaz")[1].strip()
                        label = step.split("inputuna")[0].strip().strip("'")
                        page.get_by_label(label).fill(value)
                    elif "butonuna tıkla" in step or "yazan elemana tıkla" in step:
                        text = step.split("'")[1]
                        page.get_by_text(text).click()
                    elif "saniye bekle" in step:
                        seconds = int(step.split(" ")[0])
                        page.wait_for_timeout(seconds * 1000)

                    screenshot = page.screenshot()
                    encoded = base64.b64encode(screenshot).decode("utf-8")
                    results.append({"step": step, "status": "pass", "screenshot": encoded})
                except Exception as e:
                    screenshot = page.screenshot()
                    encoded = base64.b64encode(screenshot).decode("utf-8")
                    results.append({"step": step, "status": "fail", "error": str(e), "screenshot": encoded})
                    break

            browser.close()
            logging.info("Test tamamlandı.")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, run_playwright_steps, steps)

    return {"results": results}
