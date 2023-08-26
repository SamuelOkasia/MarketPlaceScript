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
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import time
import requests
from getCar import main as getCarMain
from urllib.parse import urlparse, parse_qs

firefox_profile_path = r'C:\\Users\\ojadi\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\p4n04sri.default-release'  # Replace with the path of your Firefox profile
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

options.add_argument("-profile")
options.add_argument(firefox_profile_path)
service = Service('geckodriver.exe')
driver = Firefox(service=service, options=options)

everyday_brands_uk = [
    'Ford',
    'Vauxhall',
    'Volkswagen',
    'Toyota',
    'Nissan',
    'Honda',
    'Kia',
    'Hyundai',
    'Mazda',
    'Renault',
    'Peugeot',
    'Citroën',
    'SEAT',
    'Škoda',
    'Suzuki',
    'Fiat',
    'Mitsubishi',
    'Dacia',
    'Jeep',
    'Subaru',
    'MG'
]
base_url = "https://www.facebook.com/marketplace/category/search?maxPrice=2000&daysSinceListed=7&query={brand}&exact=false"

def main():
    for brand in everyday_brands_uk:

        with ThreadPoolExecutor(max_workers=4) as executor:
            search_url = base_url.format(brand=brand)
            driver.get(search_url)

            for count in range(5):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(0.5)

            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            last_height = driver.execute_script("return document.body.scrollHeight")
            retries = 3

            last7days = soup.find_all(class_='xkrivgy x1gryazu x1n2onr6')
            products = last7days[0].find_all(class_="x1lliihq x1iyjqo2")
            print("Products:" + str(len(products)))

            for product in products:
                try:
                    a_tag = product.find('a')
                    href = a_tag.get('href')
                    full_link = "https://www.facebook.com/" + str(href)
                    if not visited_link(full_link):
                        with open('visited_links.txt', 'a') as f:
                            f.write(str(full_link + '\n'))

                            executor.submit(getCarMain, full_link)

                except Exception as E:
                    pass


    # while True:
    #     html_source = driver.page_source
    #     soup = BeautifulSoup(html_source, 'html.parser')
    #
    #     products = soup.find_all(class_="x1lliihq x1iyjqo2")
    #     for product in products:
    #         try:
    #             a_tag = product.find('a')
    #             href = a_tag.get('href')
    #             full_link = "https://www.facebook.com/" + str(href)
    #             if not visited_link(full_link):
    #                 with open('visited_links.txt', 'a') as f:
    #                     f.write(str(full_link + '\n'))
    #
    #                 executor.submit(getCarMain, full_link)
    #
    #         except Exception as E:
    #             pass
    #     driver.execute_script("window.scrollBy(0, 1000);")

def visited_link(href):
    with open("visited_links.txt", 'r') as read_obj:
        for line in read_obj:
            if urlparse(href).path in line:
                return True
        return False
main()