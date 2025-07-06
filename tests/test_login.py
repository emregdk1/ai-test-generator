from playwright.sync_api import sync_playwright

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Tarayıcı açık kalsın
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        page.goto("https://flypgs.com")
        page.wait_for_timeout(3000)  # Sayfanın yüklenmesi için bekle
        
        # "BolBol Üye Girişi" butonuna tıklama
        page.click("text=BolBol Üye Girişi")
        
        # Modal açılmasını bekle
        page.wait_for_selector("input[placeholder='Cep Telefonu']", timeout=10000)
        
        # Cep telefonu ve parola gir
        page.fill("input[placeholder='Cep Telefonu']", "5416202270")  # Örnek numara
        page.fill("input[placeholder='Parola']", "Test1234!")         # Örnek şifre
        
        # Giriş Yap butonuna tıkla
        page.click("text=Giriş Yap")
        
        # Giriş sonrası 5 saniye bekle
        page.wait_for_timeout(5000)
        
        browser.close()

if __name__ == "__main__":
    test_login()
