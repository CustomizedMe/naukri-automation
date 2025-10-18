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
    
    try:
        # Chrome options for better compatibility
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-extensions")
        
        # Stealth Chrome options to avoid detection
        chrome_options.add_argument("--headless=new")  # Use new headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
        chrome_options.add_argument("--accept-language=en-US,en;q=0.9")
        chrome_options.add_argument("--accept-encoding=gzip, deflate, br")
        chrome_options.add_argument("--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        
        print("🌐 Using cloud-optimized Chrome configuration")
        
        # Start Chrome with robust error handling
        driver = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                print(f"🔍 Attempting to start Chrome (attempt {attempt + 1}/{max_retries})...")
                
                # Create service with better configuration
                service = Service(ChromeDriverManager().install())
                service.start()
                
                # Create driver with explicit service
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Set timeouts for better stability
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)
                
                # Test the session by getting the current URL
                driver.get("about:blank")
                print("✅ Chrome started successfully and session is valid")
                break
                
            except Exception as e:
                print(f"⚠️ Chrome startup attempt {attempt + 1} failed: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = None
                
                if attempt < max_retries - 1:
                    print("🔄 Retrying with different configuration...")
                    time.sleep(2)
                else:
                    print("❌ All Chrome startup attempts failed")
                    raise Exception(f"Failed to start Chrome after {max_retries} attempts: {e}")
        
        if not driver:
            raise Exception("Failed to create Chrome driver instance")
        
        # Execute stealth scripts to avoid detection
        try:
            # Remove webdriver property
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Override the plugins property
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            
            # Override the languages property
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            # Override the permissions property
            driver.execute_script("Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})")
            
            print("✅ Stealth measures applied successfully")
        except Exception as e:
            print(f"⚠️ Some stealth measures failed: {e}")
            pass  # Continue even if stealth measures fail
        
        # Navigate to Naukri with session validation and retry logic
        max_nav_retries = 3
        for nav_attempt in range(max_nav_retries):
            try:
                print(f"🌐 Navigating to Naukri.com (attempt {nav_attempt + 1}/{max_nav_retries})...")
                
                # Add random delay to avoid rate limiting
                import random
                delay = random.uniform(2, 5)
                time.sleep(delay)
                
                driver.get("https://www.naukri.com/")
                
                # Validate session is still active
                current_url = driver.current_url
                page_title = driver.title
                print(f"📍 Current URL: {current_url}")
                print(f"📄 Page Title: {page_title}")
                
                # Check if we got blocked
                if "Access Denied" in page_title or "blocked" in page_title.lower():
                    print(f"⚠️ Access denied on attempt {nav_attempt + 1}")
                    if nav_attempt < max_nav_retries - 1:
                        print("🔄 Retrying with different approach...")
                        time.sleep(10)  # Wait longer before retry
                        continue
                    else:
                        raise Exception("Access denied - website is blocking automated requests")
                
                # Wait for page to load
                time.sleep(5)
                break
                
            except Exception as nav_error:
                print(f"⚠️ Navigation attempt {nav_attempt + 1} failed: {nav_error}")
                if nav_attempt < max_nav_retries - 1:
                    print("🔄 Retrying navigation...")
                    time.sleep(5)
                else:
                    raise nav_error
        
        # Try to find and click login button with multiple selectors
        print("🔍 Looking for login button...")
        
        # Wait for page to fully load
        time.sleep(5)
        
        # Try multiple selectors for login button
        login_selectors = [
            (By.LINK_TEXT, "Login"),
            (By.PARTIAL_LINK_TEXT, "Login"),
            (By.XPATH, "//a[contains(text(), 'Login')]"),
            (By.XPATH, "//a[contains(text(), 'login')]"),
            (By.XPATH, "//button[contains(text(), 'Login')]"),
            (By.XPATH, "//button[contains(text(), 'login')]"),
            (By.XPATH, "//a[@href*='login']"),
            (By.XPATH, "//button[@class*='login']"),
            (By.CSS_SELECTOR, "a[href*='login']"),
            (By.CSS_SELECTOR, "button[class*='login']")
        ]
        
        login_button = None
        for selector_type, selector_value in login_selectors:
            try:
                print(f"🔍 Trying selector: {selector_type} = '{selector_value}'")
                login_button = driver.find_element(selector_type, selector_value)
                print(f"✅ Found login button with: {selector_type} = '{selector_value}'")
                break
            except:
                continue
        
        if not login_button:
            print("❌ Could not find login button with any selector")
            print("🔄 Trying direct navigation to login page...")
            
            # Try direct navigation to login page
            try:
                driver.get("https://www.naukri.com/nlogin/login")
                time.sleep(5)
                print("✅ Navigated directly to login page")
            except Exception as nav_error:
                print(f"❌ Direct navigation failed: {nav_error}")
                print("🔍 Current page source preview:")
                print(driver.page_source[:500] + "...")
                raise Exception("Login button not found and direct navigation failed")
        else:
            # Click the login button
            login_button.click()
            print("✅ Login button clicked successfully")
            time.sleep(3)
        
        print("🚀 Driver setup completed successfully")
        return driver
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        if 'driver' in locals() and driver:
            try:
                driver.quit()
            except:
                pass
        raise Exception(f"Failed to setup driver: {e}")

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
        
        # Wait for login to process
        time.sleep(8)
        
        # Check for login success/failure with comprehensive validation
        print("🔍 Validating login status...")
        
        # Check for error messages first
        error_found = False
        try:
            # Look for various error message patterns
            error_selectors = [
                "//div[contains(@class, 'error')]",
                "//div[contains(@class, 'alert')]",
                "//span[contains(@class, 'error')]",
                "//div[contains(text(), 'Invalid')]",
                "//div[contains(text(), 'Wrong')]",
                "//div[contains(text(), 'incorrect')]",
                "//div[contains(text(), 'failed')]",
                "//div[contains(text(), 'blocked')]"
            ]
            
            for selector in error_selectors:
                try:
                    error_elements = driver.find_elements(By.XPATH, selector)
                    for error_element in error_elements:
                        error_text = error_element.text.strip()
                        if error_text and len(error_text) > 0:
                            print(f"❌ Login error detected: {error_text}")
                            error_found = True
                            break
                    if error_found:
                        break
                except:
                    continue
        except:
            pass
        
        # Check current URL and page content
        current_url = driver.current_url
        page_title = driver.title
        print(f"📍 Current URL after login: {current_url}")
        print(f"📄 Page Title after login: {page_title}")
        
        # Check if we're still on login page
        if "login" in current_url.lower() or "signin" in current_url.lower():
            print("⚠️ Still on login page - login failed")
            error_found = True
        
        # Check for CAPTCHA or additional verification
        try:
            captcha_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'captcha') or contains(@id, 'captcha')]")
            if captcha_elements:
                print("⚠️ CAPTCHA detected - manual intervention required")
                error_found = True
        except:
            pass
        
        if error_found:
            print("❌ Login failed - please check credentials and try again")
            print("🔍 Debug: Current page source preview:")
            try:
                page_source = driver.page_source
                print(page_source[:1000] + "..." if len(page_source) > 1000 else page_source)
            except:
                print("Could not retrieve page source")
            raise Exception("Login failed - invalid credentials or additional verification required")
        
        # Navigate to profile page
        print("🔍 Navigating to profile page...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        
        # Final validation - check if we can access profile
        final_url = driver.current_url
        if "login" in final_url.lower() or "signin" in final_url.lower():
            print("⚠️ Redirected back to login - authentication failed")
            raise Exception("Authentication failed - unable to access profile page")
        else:
            print("🎯 Successfully navigated to profile page")
            print(f"Current URL: {final_url}")
        
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
