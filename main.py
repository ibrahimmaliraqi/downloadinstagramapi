from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def downloadFunc(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://sssinstagram.com/reels-downloader")

        # إدخال الرابط
        input_box = driver.find_element(By.ID, "input")
        input_box.clear()
        input_box.send_keys(url)

        # الضغط على زر Download
        driver.find_element(By.CSS_SELECTOR, "button.form__submit").click()

        wait = WebDriverWait(driver, 60)

        # محاولة إغلاق الإعلان إذا ظهر
        try:
            close_ad = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ad-modal__close"))
            )
            close_ad.click()
        except:
            pass

        # انتظار رابط التحميل
        download_link_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.button__download"))
        )

        return download_link_element.get_attribute("href")

    finally:
        driver.quit()

@app.route("/reel")
def getUrl():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "يجب إرسال باراميتر url"}), 400

    download_url = downloadFunc(url)
    return jsonify({"url": download_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
