from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

def test_flight_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        page.goto("https://www.flypgs.com/", timeout=60000)

        # Tek Yön butonuna tıkla
        page.wait_for_selector("text=Tek Yön")
        page.click("text=Tek Yön", force=True)

        # Nereden dropdown'unu aç ve seçim yap
        nereden_container = "div.SelectBox__control--departure"
        page.wait_for_selector(nereden_container)
        page.click(nereden_container)

        nereden_input = "input.SelectBox__form-input.tstnm_fly_search_tab_1_departure_input"
        page.wait_for_selector(nereden_input)
        page.fill(nereden_input, "SAW")
        page.wait_for_timeout(1000)

        first_option = "div.SelectBox__menu-list div.SelectBox__option"
        page.wait_for_selector(first_option)
        page.click(first_option)

        # Nereye dropdown'unu aç ve seçim yap
        nereye_container = "div.SelectBox__control--arrival"
        page.wait_for_selector(nereye_container)
        page.click(nereye_container)

        nereye_input = "input.SelectBox__form-input.tstnm_fly_search_tab_1_arrival_input"
        page.wait_for_selector(nereye_input)
        page.fill(nereye_input, "SZF")
        page.wait_for_timeout(1000)

        page.wait_for_selector(first_option)
        page.click(first_option)

        # Gidiş Tarihi seç
        gidis_tarihi_selector = "input[name='departureDate']"
        page.wait_for_selector(gidis_tarihi_selector)
        page.click(gidis_tarihi_selector, force=True)

        target_date = datetime.now() + timedelta(days=10)
        day = target_date.day

        date_selector = f"//td[@role='gridcell' and not(contains(@class, 'disabled')) and text()='{day}']"
        page.wait_for_selector(date_selector)
        page.click(date_selector)

        # Son olarak biraz bekle, sonuçları görebilmek için
        page.wait_for_timeout(10000)

        # İstersen context.close() ve browser.close() ile kapatabilirsin
        # context.close()
        # browser.close()

if __name__ == "__main__":
    test_flight_search()
