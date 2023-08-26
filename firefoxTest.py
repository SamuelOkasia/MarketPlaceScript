import time

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

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

ford = ['ford']
def main():
    for brand in everyday_brands_uk:

        with ThreadPoolExecutor(max_workers=3) as executor:
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
                    print(full_link)

                except Exception as E:
                    pass

            while False:
                # Scroll down by the height of the viewport (incremental scrolling).
                driver.execute_script("window.scrollBy(0, window.innerHeight);")

                # Wait to load the page.
                time.sleep(2)

                # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    retries -= 1
                    if retries <= 0:
                        break
                else:
                    retries = 3

                last_height = new_height
            products = soup.find_all(class_="x1lliihq x1iyjqo2")
            #print(len(products))

main()