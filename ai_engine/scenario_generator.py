import uuid
import os
import json
import openai
from pathlib import Path

def generate_test_scenario(components_path: str, output_dir: str = "outputs"):
    with open(components_path, "r", encoding="utf-8") as f:
        components = json.load(f)

    # 🧹 Temizlik: Boş selector, tag veya text içerenleri çıkar
    components = [c for c in components if c.get("text") and c.get("selector") and c.get("tag")]

    # ✂️ Token limitine takılmamak için kısıtlama
    components = components[:150]

    prompt = f"""Aşağıda bir web sayfasındaki UI bileşenlerinin JSON listesi yer almaktadır. 
Bu verilere dayanarak, anlamlı bir test senaryosu üretin:

{json.dumps(components, indent=2, ensure_ascii=False)}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sen bir kıdemli test otomasyon mühendisisin."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    output_text = response.choices[0].message["content"]
    scenario_file = os.path.join(output_dir, f"scenario_{uuid.uuid4().hex[:8]}.txt")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(scenario_file, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"✅ Test scenario generated and saved to {scenario_file}")
