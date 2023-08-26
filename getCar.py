import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import os

profile_directory = r'Profile 1'  # replace 'Profile 1' with your profile's name
user_data_dir = r"C:\Users\ojadi\AppData\Local\Google\Chrome\User Data"
chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")

chrome_options = webdriver.ChromeOptions()

chrome_options.binary_location = chrome_bin
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


API_ENDPOINT = "http://127.0.0.1:5000/api/add_product"

chrome_driver_path = os.environ.get("CHROMEDRIVER_PATH", "chromedriver")

class main():

    def __init__(self, link):
        self.link = link
        self.link = link
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        self.driver.get(link)
        self.clickSeeMoreButton()
        html_source = self.driver.page_source
        self.soup = BeautifulSoup(html_source, 'html.parser')

        self.name = self.getName("x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u")
        self.mileage = self.getAttribute("x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u", 'Driven')
        self.mileage = self.mileage.replace("Driven",'').replace("miles",'').replace('km','')

        self.transmission = self.getAttribute("x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u", 'transmission')
        self.transmission = self.transmission.replace("transmission",'')

        self.description = self.getDescription()
        self.image = self.getImage()
        self.price = self.getAttribute("x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u",'£')
        self.dateList = self.getAttribute('x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa','Listed')
        self.dateList = self.extract_time_duration()
        self.deploy()

    def getName(self,className):
        try:
            for possible_name in self.soup.find_all(class_=className):
                if possible_name.text and (possible_name.text not in ['Chats','Notifications']):
                    return possible_name.text
            return 'No name'
        except Exception as E:
            return "Couldn't even find element for name"
    def getAttribute(self,className,identifier):
        try:
            spans = self.soup.findAll(class_=className)
            for span in spans:
                if identifier in span.text:
                    return span.text
            return 'None'

        except Exception as E:
            return "Couldn't find attribute"

    def getDescription(self):
        try:
            possible_descriptions = self.soup.find_all(class_="xod5an3")
            log = 'Found a list of what could be possible descriptions'
            try:
                for description in possible_descriptions:
                    if description.find(class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84') and (description.find(class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84').text): #check if it finds a element with this class and that you can extract text
                        if description.find(class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84').text == "Seller's description":
                            log = 'Found  the label -Sellers description'
                            return description.find(class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u").text
                return log
            except:
                return "Couldn't find description"

        except:
            return "Couldn't even get a list of descriptions"

        '''
        possible_descriptions = self.soup.find_all(class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u")
        for description in possible_descriptions:
            print(description)
        '''

    def getImage(self):
        try:
            return self.soup.find('img', alt=lambda value: value and value.startswith("Product photo of"))['src']
        except:
            return None
    def clickSeeMoreButton(self):
        try:
            # Waiting for the "See more" button to be clickable
            wait = WebDriverWait(self.driver, 5)
            see_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "See more")]')))
            see_more_button.click()
        except Exception as e:
            pass
            #print(f"Error clicking the 'See more' button: {e}")

    def has_keywords(self):
        with open("keywords.txt", "r") as file:
            keywords = [line.strip().lower() for line in file.readlines()]

        for keyword in keywords:
            if keyword in self.description.lower():
                return True
        return False

    def extract_time_duration(self):
        # Look for patterns like numbers followed by words (e.g., 6 weeks, 22 hours)
        match = re.search(r'(\d+\s+\w+)', self.dateList)

        if match:
            return match.group(1)
        else:
            return None
    def deploy(self):
        if self.has_keywords():
            print(self.name, self.image)
            requests.post(API_ENDPOINT, json={"link": self.link, 'name':self.name, 'description':self.description, 'transmission':self.transmission, 'image':self.image, 'price':self.price,'mileage':self.mileage, 'listed':self.dateList})
        else:
            pass




#car = main('https://www.facebook.com/marketplace/item/668602381818078/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3Aa5eb58bf-b52c-4904-8115-01806b4442ef')
#print(car.name,car.image)
