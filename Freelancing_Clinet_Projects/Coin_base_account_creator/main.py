from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests
import time

API_KEY = 'your_2captcha_api_key'

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable blink features
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Use a legitimate User-Agent string

    # Read proxies from file
    with open('proxies.txt') as f:
        proxies = f.read().strip().split('\n')

    # Set proxy for Chrome
    if proxies:
        proxy = proxies[0]  # Select the first proxy; you can rotate proxies as needed
        chrome_options.add_argument(f'--proxy-server={proxy}')

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
        """
    })

    return driver
def element_exists(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False

def solve_captcha(driver):
    try:
        # Check if the captcha element is present and visible
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'g-recaptcha'))
        )
        if captcha_element.is_displayed():
            site_key = captcha_element.get_attribute('data-sitekey')
            current_url = driver.current_url

            # Request captcha solution from 2captcha
            response = requests.post(f'http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={site_key}&pageurl={current_url}&json=1')
            request_id = response.json().get('request')

            # Poll for the captcha result
            result = None
            while True:
                time.sleep(5)
                result_response = requests.get(f'http://2captcha.com/res.php?key={API_KEY}&action=get&id={request_id}&json=1')
                result = result_response.json()
                if result.get('status') == 1:
                    break

            # Get the response token
            response_token = result.get('request')

            # Inject the response token into the page
            driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{response_token}";')
            driver.execute_script(f'__doPostBack("g-recaptcha-response", "{response_token}");')
            time.sleep(2)  # Wait for the captcha to be processed
    except (NoSuchElementException, TimeoutException) as e:
        driver.save_screenshot("Captcha-not-found.png")
        print("Captcha not found or timeout: ", e)
    except Exception as e:
        driver.save_screenshot("Captcha not Sloved.png")
        print("Error solving captcha: ", e)

def process_email(driver, mail, passwords, password_index):
    password = passwords[password_index % len(passwords)].strip()
    actions = ActionChains(driver)
    driver.get("https://www.coinbase.com/signup")
    driver.maximize_window()
    time.sleep(0.5)
    
    # Check if the captcha is present and solve it
    try:
        driver.save_screenshot("Processing email.png")
        send_email = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'email')))
        send_email.send_keys(mail.strip())
        time.sleep(1)
        driver.save_screenshot("Processing email.png")
        
        scroll_to_bottom(driver)
        time.sleep(2)

        cookie_button_find = driver.find_elements(By.TAG_NAME, "button")
        for index, cookie in enumerate(cookie_button_find):
            if index == 4:
                cookie.click()
        driver.save_screenshot("Processing email.png")

        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        button.click()
        time.sleep(1)
        scroll_to_bottom(driver)
        driver.save_screenshot("Processing email.png")
        
        firstname = driver.find_element(By.NAME, "firstName")
        firstname.send_keys(mail[:3])
        time.sleep(0.5)
        driver.save_screenshot("Processing email.png")

        lastname = driver.find_element(By.NAME, "lastName")
        lastname.send_keys(mail[3:6])
        time.sleep(0.5)
        driver.save_screenshot("Processing email.png")

        send_password = driver.find_element(By.NAME, "password")
        send_password.send_keys(password)
        scroll_to_bottom(driver)
        driver.save_screenshot("Processing email.png")
        time.sleep(1)
        driver.save_screenshot("Processing email.png")
        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type=checkbox]")
        if not checkbox.is_selected():
            checkbox.click()
        time.sleep(1)

        button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        time.sleep(3)
        ActionChains(driver).double_click(button1).perform()
        time.sleep(3)
        driver.save_screenshot("Processing email.png")
        
        if element_exists(driver, By.CLASS_NAME, 'g-recaptcha'):
            solve_captcha(driver)

        if "An account already exists with this email address." in driver.page_source:
            with open("success.txt", "a") as success:
                driver.save_screenshot("Processing email.png")
                print("Email already exists")
                success.write(mail.strip() + "\n")
        else:
            if element_exists(driver, By.CLASS_NAME, 'g-recaptcha'):
                solve_captcha(driver)
            driver.save_screenshot("Processing email.png")
            time.sleep(15)
            if driver.current_url == "https://www.coinbase.com/setup/confirm":
                with open("failed.txt", "a") as fail:
                    driver.save_screenshot("Processing email.png")
                    print("Account created successfully")
                    fail.write(mail.strip() + "\n")
            else:
                if element_exists(driver, By.CLASS_NAME, 'g-recaptcha'):
                    solve_captcha(driver)
                json_message = "hey"
                pas_elements = driver.find_elements(By.TAG_NAME, "p")
                for i, p in enumerate(pas_elements):
                    if i == 1:
                        json_message = p.text
                if "JSON" in json_message:
                    driver.save_screenshot("Processing email.png")
                    print("JSON error; please try to change your IP")
                    with open("failed.txt", "a") as fail:
                        fail.write(mail.strip() + "\n")
                else:
                    if element_exists(driver, By.CLASS_NAME, 'g-recaptcha'):
                        solve_captcha(driver)
                    print("Nothing happened and other error")
                    time.sleep(60)
                    driver.save_screenshot("Nothing happened.png")
                    
    except Exception as e:
        print(f"Error processing email: {e}")
        with open("error.txt", "a") as fail:
            fail.write(mail.strip() + "\n")
            driver.save_screenshot("Error_processing.png")
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)  # Adjust time delay as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def main():
    with open("emails.txt") as f_mail, open("passwords.txt") as f_password:
        emails = f_mail.readlines()
        passwords = f_password.readlines()

    for index, mail in enumerate(emails):
        driver = initialize_driver()
        password_index = index % len(passwords)
        process_email(driver, mail, passwords, password_index)
        driver.quit()

if __name__ =='__main__':
    main()