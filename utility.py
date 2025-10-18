from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver # Import WebDriver for type hinting
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # Keep By import if used in functions
import time
import os
from datetime import datetime


def switch_to_new_window(driver: WebDriver, timeout: int = 10) -> None:
    """
    Switches to a new window/tab that opens after clicking a link.
    
    Args:
        driver: The webdriver instance.
        timeout: Maximum time to wait for new window.
    """
    original_window = driver.current_window_handle
    wait = WebDriverWait(driver, timeout)
    
    # Wait for new window to open
    wait.until(lambda driver: len(driver.window_handles) > 1)
    
    # Switch to the new window
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break


def setup_driver() -> WebDriver:
    """
    Sets up and returns a configured Chrome webdriver instance.

    Returns:
        A configured Chrome webdriver instance.
    """
    import os
    import platform
    import tempfile
    
    # Chrome options for better compatibility
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-extensions")
    
    # Check if running in cloud environment (GitHub Actions)
    import os
    is_cloud = os.getenv('GITHUB_ACTIONS') is not None
    
    if is_cloud:
        # Cloud-friendly options (no user data directory)
        chrome_options.add_argument("--headless")  # Run in headless mode for cloud
        chrome_options.add_argument("--no-sandbox")  # Required for cloud environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--disable-gpu")  # Disable GPU in headless mode
        chrome_options.add_argument("--disable-web-security")  # Disable web security for cloud
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")  # Disable display compositor
        chrome_options.add_argument("--single-process")  # Run in single process mode
    else:
        # Local environment - use temporary user data directory
        temp_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        chrome_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
    
    # Try to use existing Chrome profile if possible
    try:
        print("🔍 Attempting to start Chrome with profile...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome started successfully")
    except Exception as e:
        print(f"⚠️ Chrome startup issue: {e}")
        print("🔄 Trying with minimal options...")
        
        # Fallback with minimal options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        
        if is_cloud:
            # Cloud-friendly fallback options
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--single-process")
        else:
            # Local fallback options
            chrome_options.add_argument("--remote-debugging-port=9222")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome started with minimal options")
    
    # Execute script to remove webdriver property
    try:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    except:
        pass  # Ignore if this fails
    
    driver.get("https://www.naukri.com/")
    driver.maximize_window()
    time.sleep(3)
    
    # Click login button
    login_button = driver.find_element(By.LINK_TEXT, "Login")
    login_button.click()
    time.sleep(3)
    
    print("🚀 Driver setup completed")
    return driver

def login_with_google(driver: WebDriver, email: str) -> None:
    """
    Logs in to Naukri using Google OAuth authentication.

    Args:
        driver: The webdriver instance.
        email: The user's Google email address.
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        # Look for Google login button
        google_login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Google') or contains(@class, 'google') or contains(@id, 'google')]"))
        )
        google_login_button.click()
        print("🔍 Clicked Google login button")
        time.sleep(3)
        
        # Handle Google login popup/redirect
        # Check if new window opened (popup) or if it's a redirect
        if len(driver.window_handles) > 1:
            print("🔄 Switching to Google login popup window")
            switch_to_new_window(driver)
        
        # Wait for Google login page to load
        time.sleep(3)
        
        # Check if Google account selection page appears (user already logged in)
        try:
            # Look for account selection elements
            account_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'account') or contains(@class, 'profile') or contains(@class, 'user')]")
            if account_elements:
                print("🔍 Found Google account selection page")
                # Look for the specific email account or click the first available account
                try:
                    # Try to find account with matching email
                    target_account = driver.find_element(By.XPATH, f"//div[contains(text(), '{email}')]")
                    target_account.click()
                    print(f"✅ Selected account: {email}")
                except:
                    # If specific email not found, click the first available account
                    first_account = driver.find_element(By.XPATH, "//div[contains(@class, 'account') or contains(@class, 'profile')]")
                    first_account.click()
                    print("✅ Selected first available Google account")
                
                time.sleep(3)
                
                # Check if we need to click "Continue" or similar button
                try:
                    continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Next') or contains(text(), 'Allow')]")
                    continue_button.click()
                    print("✅ Clicked Continue/Allow button")
                    time.sleep(3)
                except:
                    print("ℹ️ No continue button found, proceeding...")
                
                # Wait for redirect back to Naukri
                time.sleep(5)
                
                # If we're in a popup window, switch back to main window
                if len(driver.window_handles) > 1:
                    print("🔄 Switching back to main Naukri window")
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
                
                # Navigate to profile page
                driver.get("https://www.naukri.com/mnjuser/profile")
                time.sleep(5)
                print("🎯 Navigated to profile page")
                return
                
        except Exception as account_error:
            print(f"ℹ️ No account selection found: {account_error}")
        
        # If no account selection, proceed with manual login
        print("🔐 Proceeding with manual Google login...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        
        # Enter email
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        email_input.clear()
        email_input.send_keys(email)
        print(f"📧 Entered email: {email}")
        
        # Click Next button
        next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'next')]")
        next_button.click()
        time.sleep(3)
        
        # For Google login, we might need to handle 2FA or password
        # This is simplified - in real scenario, you might need to handle 2FA
        print("⚠️ Manual Google login requires additional steps (2FA, password, etc.)")
        print("💡 Consider using existing Chrome session for automatic login")
        
        # Wait for redirect back to Naukri
        time.sleep(5)
        
        # If we're in a popup window, switch back to main window
        if len(driver.window_handles) > 1:
            print("🔄 Switching back to main Naukri window")
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)
        
        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        print("🎯 Navigated to profile page")
        
    except Exception as e:
        print(f"❌ Google login failed: {e}")
        raise


def login_with_email_password(driver: WebDriver, email: str, password: str) -> None:
    """
    Logs in to Naukri using email and password.

    Args:
        driver: The webdriver instance.
        email: The user's email address.
        password: The user's password.
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        print("🔍 Looking for email input field...")
        # Find email input field with multiple possible selectors
        email_selectors = [
            "//input[@type='text']",
            "//input[@name='email']", 
            "//input[@id='email']",
            "//input[@placeholder='Email ID']",
            "//input[contains(@class, 'email')]"
        ]
        
        email_input = None
        for selector in email_selectors:
            try:
                email_input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                print(f"✅ Found email input with selector: {selector}")
                break
            except:
                continue
        
        if not email_input:
            print("❌ Could not find email input field")
            print("🔍 Current page URL:", driver.current_url)
            print("🔍 Page title:", driver.title)
            raise Exception("Email input field not found")
        
        email_input.clear()
        email_input.send_keys(email)
        print(f"📧 Entered email: {email}")
        
        print("🔍 Looking for password input field...")
        # Find password input field
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        password_input.clear()
        password_input.send_keys(password)
        print("🔒 Entered password")
        
        print("🔍 Looking for login button...")
        # Click login button with multiple possible selectors
        login_selectors = [
            "//button[contains(text(), 'Login')]",
            "//button[contains(text(), 'Sign In')]",
            "//input[@type='submit']",
            "//button[@type='submit']"
        ]
        
        login_button = None
        for selector in login_selectors:
            try:
                login_button = driver.find_element(By.XPATH, selector)
                print(f"✅ Found login button with selector: {selector}")
                break
            except:
                continue
        
        if not login_button:
            print("❌ Could not find login button")
            raise Exception("Login button not found")
        
        login_button.click()
        print("✅ Clicked login button")
        time.sleep(5)
        
        # Check if login was successful by looking for error messages or success indicators
        try:
            # Look for error messages
            error_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(text(), 'Invalid') or contains(text(), 'Wrong')]")
            if error_elements:
                print("⚠️ Login error detected:", error_elements[0].text)
        except:
            pass
        
        # Navigate to profile page
        print("🔍 Navigating to profile page...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        
        # Check if we're actually logged in
        current_url = driver.current_url
        if "login" in current_url.lower() or "signin" in current_url.lower():
            print("⚠️ Still on login page - login may have failed")
            print(f"Current URL: {current_url}")
        else:
            print("🎯 Successfully navigated to profile page")
            print(f"Current URL: {current_url}")
        
    except Exception as e:
        print(f"❌ Email/Password login failed: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        raise


def login_with_otp(driver: WebDriver, phone_number: str) -> None:
    """
    Logs in to Naukri using OTP (One Time Password) sent to phone.

    Args:
        driver: The webdriver instance.
        phone_number: The user's phone number.
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        # Look for OTP login option
        otp_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OTP') or contains(text(), 'Mobile') or contains(text(), 'Phone')]"))
        )
        otp_button.click()
        print("🔍 Clicked OTP login button")
        time.sleep(3)
        
        # Enter phone number
        phone_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @name='mobile' or @id='mobile']"))
        )
        phone_input.clear()
        phone_input.send_keys(phone_number)
        print(f"📱 Entered phone number: {phone_number}")
        
        # Click send OTP button
        send_otp_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send OTP') or contains(text(), 'Get OTP')]")
        send_otp_button.click()
        print("📤 OTP sent to phone")
        
        # Wait for user to enter OTP manually
        print("⏳ Please enter the OTP received on your phone...")
        input("Press Enter after entering the OTP in the browser...")
        
        # Click verify/login button
        verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify') or contains(text(), 'Login')]")
        verify_button.click()
        print("✅ OTP verified")
        time.sleep(5)
        
        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        print("🎯 Navigated to profile page")
        
    except Exception as e:
        print(f"❌ OTP login failed: {e}")
        raise


def login(driver: WebDriver, login_method: str, **kwargs) -> None:
    """
    Main login function that routes to the appropriate login method.

    Args:
        driver: The webdriver instance.
        login_method: The login method to use ('google', 'email_password', 'otp').
        **kwargs: Additional arguments for specific login methods.
    """
    print(f"🔐 Starting login with method: {login_method}")
    
    if login_method.lower() == 'google':
        email = kwargs.get('email')
        if not email:
            raise ValueError("Email is required for Google login")
        login_with_google(driver, email)
        
    elif login_method.lower() == 'email_password':
        email = kwargs.get('email')
        password = kwargs.get('password')
        if not email or not password:
            raise ValueError("Email and password are required for email/password login")
        login_with_email_password(driver, email, password)
        
    elif login_method.lower() == 'otp':
        phone_number = kwargs.get('phone_number')
        if not phone_number:
            raise ValueError("Phone number is required for OTP login")
        login_with_otp(driver, phone_number)
        
    else:
        raise ValueError(f"Unsupported login method: {login_method}. Supported methods: google, email_password, otp")

def refresh_profile(driver: WebDriver, resume_file_path: str) -> None:
    """
    Refreshes the Naukri profile by re-uploading the resume.

    Args:
        driver: The webdriver instance.
        resume_file_path: The path to the resume file.
    """
    wait = WebDriverWait(driver, 15)
    try:
        upload_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        upload_input.send_keys(resume_file_path)
        print("📎 Resume re-uploaded.")
        time.sleep(5)
        print(f"✅ Profile refreshed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print("⚠️ Could not refresh profile:", e)

def cleanup(driver: WebDriver) -> None:
    """
    Closes the webdriver instance.

    Args:
        driver: The webdriver instance.
    """
    driver.quit()
    print("✅ Script finished")
