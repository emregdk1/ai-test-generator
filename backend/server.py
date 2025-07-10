from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import base64
import re
import json
from backend.utils.selector_mapper import map_natural_step
from backend.utils.page_analyzer import analyze_page_elements

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Step(BaseModel):
    action: str
    selector: Optional[str] = None
    value: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    milliseconds: Optional[int] = None


@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    url = data.get("url")

    if not url and "steps_text" in data:
        match = re.search(r"(https?://[^\s]+)", data["steps_text"])
        if match:
            url = match.group(1)

    if not url:
        raise HTTPException(status_code=422, detail="URL zorunludur")

    try:
        elements = await analyze_page_elements(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sayfa analiz hatası: {str(e)}")

    steps = []
    if "steps_text" in data:
        for line in data["steps_text"].splitlines():
            line = line.strip()
            if not line:
                continue
            mapped = map_natural_step(line, elements)
            if mapped.get("action") and mapped["action"] != "unknown" and (mapped.get("selector") is not None or mapped["action"] == "goto" or mapped["action"] == "wait"):
                steps.append(mapped)
    else:
        steps = [{
            "action": "goto",
            "url": url,
            "description": f"Siteyi aç {url}"
        }]

    return {"steps": steps}


@app.post("/run-test")
async def run_test(steps: List[Step]):
    with open("generated_steps.json", "w", encoding="utf-8") as f:
        json.dump([s.dict() for s in steps], f, indent=2, ensure_ascii=False)

    try:
        result = subprocess.run(
            ["python", "runner.py"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)

    with open("test_result.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    for r in results:
        if r.get("screenshot_path"):
            with open(r["screenshot_path"], "rb") as img_file:
                r["screenshot"] = base64.b64encode(img_file.read()).decode("utf-8")

    return {"results": results}
