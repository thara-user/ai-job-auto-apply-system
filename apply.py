from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def auto_apply():
    # ✅ Auto download correct driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("https://www.w3schools.com/html/html_forms.asp")

    time.sleep(3)

    # Fill form
    driver.find_element(By.NAME, "firstname").send_keys("Tharani")
    driver.find_element(By.NAME, "lastname").send_keys("AI")

    print("Form filled successfully!")

    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    auto_apply()
