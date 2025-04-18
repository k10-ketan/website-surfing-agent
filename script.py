from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

def selenium_task():
    options = ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    # Perform the selenium task
    driver.get("http://www.python.org")
    assert "Python" in driver.title

    page_source = driver.page_source

    driver.close()
    return page_source

if __name__ == '__main__':
    page_source = selenium_task()
    print(page_source)