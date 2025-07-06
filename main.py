import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from analyzer.web_analyzer import analyze_page
from ai_engine.scenario_generator import generate_test_scenario
from ai_engine.generate_playwright_test import generate_playwright_test

if __name__ == "__main__":
    url = input("🔗 Test edilecek web sayfasının URL’sini girin: ")
    analyze_page(url)
    generate_test_scenario("data/components.json")

generate_playwright_test("data/components.json", "tests/test_generated.py")

