from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup


'''
firefox_profile_path = r'C:\\Users\\ojadi\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\p4n04sri.default-release'  # Replace with the path of your Firefox profile
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

options.add_argument("-profile")
options.add_argument(firefox_profile_path)
service = Service('geckodriver.exe')
driver = Firefox(service=service, options=options)
'''

#Start
import os
from selenium import webdriver
firefox_bin = os.environ.get("FIREFOX_BIN", "firefox")  # Default to "firefox" if not set

options = webdriver.FirefoxOptions()
options.binary_location = firefox_bin
options.add_argument("--headless")

# The service uses the GECKODRIVER_PATH provided by the buildpack
service = webdriver.firefox.service.Service(os.environ.get("GECKODRIVER_PATH"))
driver = webdriver.Firefox(service=service, options=options)
#Stop

driver.get("https://www.facebook.com/marketplace/london/search?query=vw%20polo")
time.sleep(5)

html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')


time.sleep(3)
c=0
while c < 10:

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    c +=1
    time.sleep(3)
    print(c)


time.sleep(4)
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

print(len(soup.find_all(class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")))