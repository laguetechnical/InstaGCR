from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
import random
import threading
from selenium.webdriver.common.keys import Keys

num = int(input("which profile to use ?? "))

def click_changebt(driver):
    """
    Clicks the 'Change group name' button in Instagram GC settings.
    Uses aria-label instead of long XPath for maximum stability.
    """

    try:
        # Wait until the button appears
        btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Change group name']"))
        )

        # Click using JavaScript for 100% reliability
        driver.execute_script("arguments[0].click();", btn)

        print("✔ Change button clicked")

    except Exception as e:
        print("❌ Failed to click Change button:", e)

def write_name(driver, name):
    try:
        name_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Group name']"))
        )

        # FORCE CLEAR (React-compatible)
        name_input.send_keys(Keys.CONTROL + "a")
        time.sleep(0.1)
        name_input.send_keys(Keys.DELETE)
        time.sleep(0.2)

        # Type new name
        name_input.send_keys(name)

        print(f"✔ Group name updated to: {name}")

    except Exception as e:
        print("❌ Could not write group name:", e)
def clicksave(driver):
    """
    Clicks the real enabled 'Save' button in Instagram.
    Works even when Instagram replaces the button element dynamically.
    """

    try:
        # Wait for ENABLED Save button (role=button and text()='Save')
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Save']"))
        )

        # Click using JS (most reliable)
        driver.execute_script("arguments[0].click();", button)

        print("✔ Save button clicked")

    except Exception as e:
        print("❌ Failed to click Save button:", e)
def click_instagram_group_info(driver):
    try:
        # Wait until the SVG becomes visible in the DOM
        icon = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Conversation information']"))
        )

        # Find the parent button
        button = icon.find_element(By.XPATH, "./ancestor::div[@role='button'][1]")

        # Click using JS (most reliable)
        driver.execute_script("arguments[0].click();", button)

        print("✔ Group Info button clicked")

    except Exception as e:
        print("❌ Could not click Group Info:", e)
def is_logged_in(driver):
        try:
            # Instagram logged-in homepage contains the "Home" button with aria-label="Home"
            driver.find_element(By.XPATH, "//a[contains(@href, '/accounts/edit/') or @aria-label='Home']")
            return True
        except:
            return False
for i in range(1):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1000,800")
    options.add_argument("--mute-audio")
    options.add_argument(f"--remote-debugging-port={9222 + num}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)
    profile_path = os.path.abspath(f"profile_{num}")
    os.makedirs(profile_path, exist_ok=True)
    options.add_argument(f"--user-data-dir={profile_path}")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://instagram.com/")
    while not is_logged_in(driver):
        print("\n❗ You are NOT logged in.")
        print("👉 Please login manually in the browser window.")
        input("✔ After logging in successfully, press ENTER to continue...")

    print("\n✅ Logged in successfully! Continuing script...")
    thread_id = input("Enter Group Thread ID: ").strip()
    gc_url = f"https://www.instagram.com/direct/t/{thread_id}/"
    driver.get(gc_url)

    click_instagram_group_info(driver)
    testlist = ["name1", "name2", "name3", "name4", "name5", "name6", "name7", "name8", "name9", "name10", "name11"]
    list1 = ["AHMED PAPA ZINDABAD!!! ", "AHMED PAPA HAI TERAAA", "TERA BAP KON ? AHMED JI !!", "PURE GC KA PAPA KON? AHMED PAPAAA"]
    list2 = ["oyeee, anddd", "manddd", "kaa", "tolaa", "terii", "behen ka", "lolaa"]
    list3 = ["tere abba ki choodiya", "terri mada choot chaatu", "oye tor maike chut chaat", "tere dada ki gand maru", "tere dada ki gend me loda loda loda"]

    choice = int(input("Which list to use?      "))
    print("0) testlist\n 1)list1\n2) list2\n3) list3")
    if choice==0:
        while True:
            for name in testlist:

                print(f"\n➡ Changing name to: {name}")

                click_changebt(driver)
                write_name(driver, name)
                clicksave(driver)
    elif choice==1:
        while True:
            for name in list1:

                print(f"\n➡ Changing name to: {name}")

                click_changebt(driver)
                write_name(driver, name)
                clicksave(driver)
    elif choice==2:
        while True:
            for name in list2:

                print(f"\n➡ Changing name to: {name}")

                click_changebt(driver)
                write_name(driver, name)
                clicksave(driver)
    elif choice==3:
        while True:
            for name in list3:

                print(f"\n➡ Changing name to: {name}")

                click_changebt(driver)
                write_name(driver, name)
                clicksave(driver)