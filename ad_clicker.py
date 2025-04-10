import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

# ---------- CONFIG ----------
LOOP_COUNT = 5
TARGET_URL = "https://animesamaj.blogspot.com/?m=1"

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1"
]

SCREEN_SIZES = [
    (375, 667), (414, 896), (390, 844), (768, 1024), (1920, 1080)
]

# ---------- STEALTH.JS INJECTION ----------
def inject_stealth_js(driver):
    stealth_js = """
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    Object.defineProperty(navigator, 'mimeTypes', { get: () => [{type: "application/pdf"}, {type: "application/x-google-chrome-pdf"}] });
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 4 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
    Object.defineProperty(screen, 'width', { get: () => 390 });
    Object.defineProperty(screen, 'height', { get: () => 844 });
    Intl.DateTimeFormat.prototype.resolvedOptions = function () {
        return { timeZone: 'Asia/Kolkata' };
    };
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return "Intel Inc.";
        if (parameter === 37446) return "Intel Iris OpenGL Engine";
        return getParameter.call(this, parameter);
    };
    console.log("✅ Stealth script injected.");
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_js})

# ---------- MAIN LOOP ----------
for i in range(LOOP_COUNT):
    print(f"\n🔁 Loop {i+1} of {LOOP_COUNT}")

    user_agent = random.choice(USER_AGENTS)
    screen_width, screen_height = random.choice(SCREEN_SIZES)

    print(f"🧠 UA: {user_agent}")
    print(f"📱 Screen: {screen_width}x{screen_height}")

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options, headless=False, use_subprocess=True)
    inject_stealth_js(driver)
    driver.set_window_size(screen_width, screen_height)

    driver.get(TARGET_URL)
    time.sleep(random.uniform(5, 7))

    actions = ActionChains(driver)
    black_clicked = False
    original_tabs = driver.window_handles

    print("👀 Searching for black ad zones...")
    black_elements = driver.find_elements(By.XPATH, "//*[contains(@style,'background-color: rgb(0, 0, 0)') or contains(@style,'background: black')]")

    for elem in black_elements:
        try:
            if elem.is_displayed() and elem.is_enabled():
                location = elem.location_once_scrolled_into_view
                size = elem.size
                print("🖱️ Clicking black ad...")
                actions.move_to_element_with_offset(elem, 5, 5).pause(1).click().perform()
                black_clicked = True
                break
        except:
            continue

    if not black_clicked:
        print("⚠️ No black found. Trying fallback...")
        fallback = driver.find_elements(By.XPATH, "//a | //button | //div[@onclick]")
        for el in fallback:
            try:
                if el.is_displayed() and el.is_enabled():
                    actions.move_to_element(el).pause(1).click().perform()
                    print("🖱️ Clicked fallback element.")
                    break
            except:
                continue

    # Detect tab switch after ad click
    time.sleep(2)
    new_tabs = driver.window_handles
    if len(new_tabs) > len(original_tabs):
        print("🆕 New tab opened! Switching and waiting 30s...")
        driver.switch_to.window(new_tabs[-1])
        time.sleep(30)
        driver.switch_to.window(new_tabs[0])
    else:
        print("⏳ No new tab. Proceeding to close...")

    print("🛑 Closing Chrome for this loop.")
    driver.quit()
