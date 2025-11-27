import logging
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging to handle Unicode characters
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - Thread: %(threadName)s',
    handlers=[
        logging.FileHandler('group_name_changer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_driver():
    logger.debug("Setting up Chrome WebDriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-extensions")
    # options.add_argument("--headless")  # Uncomment for headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    logger.debug("Chrome WebDriver initialized")
    return driver

def login_ac(driver, thread_name):
    logger.info(f"Initiating login process for {thread_name}")
    try:
        driver.get('https://www.instagram.com/accounts/login/')
        logger.debug("Navigated to Instagram login page")
        input(f"Press Enter after manual login for {thread_name}...")
        logger.info("Manual login completed")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logger.debug("Login page fully loaded")
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise

def change_group_name(driver, url, group_names):
    logger.info(f"Starting group name change process for URL: {url}")
    
    try:
        # Navigate to group chat
        logger.debug(f"Navigating to group chat URL: {url}")
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logger.info("Group chat page opened successfully")
        
        # Attempt to open sidebar
        try:
            logger.debug("Looking for Conversation information button")
            sidebar_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div[3]'
                ))
            )
            sidebar_button.click()
            logger.info("Sidebar opened successfully")
        except TimeoutException:
            logger.warning("Conversation information button not found")
            try:
                logger.debug("Checking if sidebar content is already visible")
                sidebar_content = driver.find_element(
                    By.XPATH,
                    '//div[contains(@class, "x7r02ix x15fl9t6 x1yw9sn2")]'
                )
                logger.info("Sidebar content already visible")
            except NoSuchElementException:
                logger.error("Sidebar could not be opened and content not found")
                input(f"Press Enter to continue or Ctrl+C to exit for {url}...")
                return

        # Continuous loop through group names
        index = 0
        while True:
            name = group_names[index % len(group_names)]  # Cycle through names
            logger.info(f"Attempting to change group name to: {name}")

            try:
                # Step 1: Try to find the "Change group name" button
                logger.debug("Looking for Change group name button")
                change_button = None
                try:
                    change_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            '//div[@aria-label="Change group name"]'
                        ))
                    )
                except TimeoutException:
                    logger.warning("Change group name button not found, checking for dialog")

                # Step 2: If change button not found, check for dialog/input/save
                if not change_button:
                    try:
                        logger.debug("Checking for group name change dialog")
                        dialog = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                '//div[contains(@class, "x7r02ix x15fl9t6 x1yw9sn2")]'
                            ))
                        )
                        logger.debug("Dialog found, attempting to process input and save")
                        try:
                            input_field = dialog.find_element(
                                By.XPATH,
                                '//input[@aria-label="Group name"]'
                            )
                            # Use JavaScript to clear input field
                            driver.execute_script("arguments[0].value = ''", input_field)
                            input_field.send_keys(name)
                            logger.info(f"Entered new group name: {name}")

                            try:
                                save_button = dialog.find_element(
                                    By.XPATH,
                                    '//div[@role="button" and contains(text(), "Save")]'
                                )
                                save_button.click()
                                logger.info("Save button clicked")
                                index += 1
                                continue
                            except (TimeoutException, NoSuchElementException):
                                logger.warning("Save button not found, restarting loop")
                                continue
                        except NoSuchElementException:
                            logger.warning("Input field not found, restarting loop")
                            continue
                    except TimeoutException:
                        logger.warning("Dialog not found, restarting loop")
                        continue

                # Step 3: If change button found, proceed with normal flow
                change_button.click()
                logger.info("Change group name button clicked")

                # Step 4: Wait for dialog and input field
                try:
                    logger.debug("Waiting for group name change dialog")
                    dialog = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            '//div[contains(@class, "x7r02ix x15fl9t6 x1yw9sn2")]'
                        ))
                    )
                    try:
                        input_field = dialog.find_element(
                            By.XPATH,
                            '//input[@aria-label="Group name"]'
                        )
                        # Use JavaScript to clear input field
                        driver.execute_script("arguments[0].value = ''", input_field)
                        input_field.send_keys(name)
                        logger.info(f"Entered new group name: {name}")

                        try:
                            save_button = dialog.find_element(
                                By.XPATH,
                                '//div[@role="button" and contains(text(), "Save")]'
                            )
                            save_button.click()
                            logger.info("Save button clicked")
                            WebDriverWait(driver, 10).until(
                                EC.invisibility_of_element_located((
                                    By.XPATH,
                                    '//div[contains(@class, "x7r02ix x15fl9t6 x1yw9sn2")]'
                                ))
                            )
                            logger.debug("Group name change dialog closed")
                        except (TimeoutException, NoSuchElementException):
                            logger.warning("Save button not found, attempting to recover")
                            try:
                                input_field = dialog.find_element(
                                    By.XPATH,
                                    '//input[@aria-label="Group name"]'
                                )
                                driver.execute_script("arguments[0].value = ''", input_field)
                                input_field.send_keys(name)
                                logger.info(f"Re-entered new group name: {name}")
                                try:
                                    save_button = dialog.find_element(
                                        By.XPATH,
                                        '//div[@role="button" and contains(text(), "Save")]'
                                    )
                                    save_button.click()
                                    logger.info("Save button clicked after retry")
                                    WebDriverWait(driver, 10).until(
                                        EC.invisibility_of_element_located((
                                            By.XPATH,
                                            '//div[contains(@class, "x7r02ix x15fl9t6 x1yw9sn2")]'
                                        ))
                                    )
                                    logger.debug("Group name change dialog closed")
                                except (TimeoutException, NoSuchElementException):
                                    logger.warning("Save button still not found, restarting loop")
                                    continue
                            except NoSuchElementException:
                                logger.warning("Input field not found on retry, restarting loop")
                                continue
                    except NoSuchElementException:
                        logger.warning("Input field not found, restarting loop")
                        continue
                except TimeoutException:
                    logger.warning("Dialog not found after clicking change button, restarting loop")
                    continue

                index += 1

            except Exception as e:
                logger.error(f"Error during group name change: {str(e)}")
                input(f"Press Enter to continue or Ctrl+C to exit for {url}...")
                continue

    except KeyboardInterrupt:
        logger.info("Continuous name change stopped by user")
        return
    except Exception as e:
        logger.error(f"Critical error in change_group_name: {str(e)}")
        raise

def run_instance(url, group_names, thread_name):
    driver = setup_driver()
    try:
        login_ac(driver, thread_name)
        change_group_name(driver, url, group_names)
    except Exception as e:
        logger.error(f"Error in instance for URL {url}: {str(e)}")
    finally:
        logger.debug("Cleaning up: Closing WebDriver")
        driver.quit()
        logger.info("WebDriver closed")

def main():
    logger.info("Starting Group Name Changer Tool by Ahmed Bhai")
    
    instances = [
        {
            "url": "https://www.instagram.com/direct/t/9827917957331340/",
            "group_names": [
                "AHMED PAPA ZINDABAD !",
                "AHMED PAPA ZINDABAD !!",
                "AHMED BHAI KI JAI HO !!!",
                "AHMED BHAI KI JAI HO !!!!",
                "AHMED BHAI KI JAI HO !!!!!",
                "AHMED BHAI KI JAI HO !!!!!!"
            ]
        },
        {
            "url": "https://www.instagram.com/direct/t/9827917957331340/",  # Replace with actual group URL
            "group_names": [
                "AHMED PAPA ZINDABAD !!!!!!!",
                "AHMED PAPA ZINDABAD !!!!!!!!",
                "AHMED BHAI KI JAI HO !!!!!!!!",
                "AHMED BHAI KI JAI HO !!!!!!!!!",
                "AHMED BHAI KI JAI HO !!!!!!!!!!",
                "AHMED BHAI KI JAI HO !!!!!!!!!!!"
            ]
        }
    ]

    threads = []
    for i, instance in enumerate(instances, 1):
        thread_name = f"Thread-Group{i}"
        thread = threading.Thread(
            target=run_instance,
            args=(instance["url"], instance["group_names"], thread_name),
            name=thread_name
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    logger.info("All instances completed")

if __name__ == "__main__":
    main()