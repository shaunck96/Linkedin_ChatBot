from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

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


driver.get("https://www.linkedin.com/in/sanjana-athreya/recent-activity/all/")

driver.implicitly_wait(10)

# Set sleep time for the page to load on scroll
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# If you want to limit the number of scroll loads, add a limit here
scroll_limit = 20

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

# Extracting all the posts
posts = soup.find_all("div", {'class': 'update-components-text relative update-components-update-v2__commentary'})

a_tags = soup.find_all('a', class_='app-aware-link update-components-actor__sub-description-link')
date_of_post = [tag.get('aria-label') for tag in a_tags]

#like_counts = soup.find_all("div", {'class': 'update-v2-social-activity'})
# Find the element with the specified class
like_counts = []
reactions_elements = soup.find_all('li', class_='social-details-social-counts__reactions')
for reactions_element in reactions_elements:
    like_count = reactions_element.find('button').text.strip()
    like_counts.append(like_count)

post_info_df = pd.DataFrame(columns=['post_info', 'date_of_post', 'like_count'])

index = 0
for post in posts:
    post_info_df.at[index, 'post_info'] = post.text
    index+=1

index=0    
for date in date_of_post:    
    post_info_df.at[index, 'date_of_post'] = date
    
index=0     
for like_count in like_counts:    
    post_info_df.at[index, 'like_count'] = like_count
    index += 1

post_info_df.to_csv(r'post_details.csv')
driver.quit()
