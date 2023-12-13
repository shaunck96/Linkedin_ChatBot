from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

email = "shaunchackoofficial@gmail.com"
password = "Chacko1234#"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chrome_options)#,executable_path="chromedriver.exe")
driver.maximize_window()
driver.get('https://www.linkedin.com/login')
time.sleep(10)

driver.find_element(By.ID, 'username').send_keys("shaunchackoofficial@gmail.com")
driver.find_element(By.ID, 'password').send_keys("Chacko1234#")

driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
time.sleep(10)


driver.get("https://www.linkedin.com/in/sanjana-athreya/")

driver.implicitly_wait(10)

# Set sleep time for the page to load on scroll
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# If you want to limit the number of scroll loads, add a limit here
scroll_limit = 10

count = 0

while True and count < scroll_limit:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    count += 1

src = driver.page_source

# Now using BeautifulSoup
soup = BeautifulSoup(src, 'html.parser')  # Use 'html.parser' instead of 'lxml'

# Extracting titles
titles_divs = soup.find_all("div", {'class': 'display-flex align-items-center mr1 t-bold'})
job_description = soup.find_all("div", {'class': 'pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center'})

# Extracting the text from each title div
titles = []
for div in titles_divs:
    span = div.find('span', {'aria-hidden': 'true'})
    if span:
        titles.append(span.text.strip())
        
descriptions = []
for div in job_description:
    span = div.find('span', {'aria-hidden': 'true'})
    if span:
        descriptions.append(span.text.strip())

output = {}
output['Descriptions'] = descriptions
output['Titles'] = titles

with open("profile_data.json", "w") as json_file:
    json.dump(output, json_file)

driver.quit()
