import json
import openai

def generate_scenario(components, page_type, target):
    # Bileşenleri filtrele
    filtered = [
        c for c in components if c.get("text") or c.get("aria-label") or c.get("placeholder")
    ][:150]  # token sınırını aşmamak için sınırla

    prompt = f"""
Aşağıdaki JSON, bir '{page_type}' sayfasındaki web bileşenlerini temsil etmektedir.
Senin görevin, bu bileşenleri kullanarak '{target}' hedefini gerçekleştirecek bir test senaryosu üretmektir.
Adımlar sade ve anlaşılır olsun. Adımları JSON formatında bir dizi (array) olarak döndür.

Bileşen listesi:
{json.dumps(filtered, indent=2, ensure_ascii=False)}

Lütfen sadece aşağıdaki formatta JSON döndür:

[
  "Siteyi aç https://example.com",
  "'Kullanıcı Adı' inputuna testuser yaz",
  "'Şifre' inputuna secret123 yaz",
  "'Giriş Yap' butonuna tıkla",
  "3 saniye bekle"
]
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sen deneyimli bir test otomasyon mühendisisin."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    try:
        generated = response.choices[0].message["content"]
        steps = json.loads(generated)
        assert isinstance(steps, list)
        return steps
    except Exception as e:
        print(f"⚠️ Yanıt parse edilemedi: {e}")
        return []
