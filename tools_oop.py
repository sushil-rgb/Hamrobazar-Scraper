from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from time import sleep
import random


scrape_range = 50
# Get random user-agent for scraping:
def get_user_agent():
    ua_strings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 "
        "Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 "
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 "
        "Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
    ]
 
    return random.choice(ua_strings)


class HamrobazarScraper:


    def __init__(self, url):
        self.headers = {'User-Agent':get_user_agent()}
        self.url = url
        self.req = requests.get(url, headers=self.headers)

        # Setting up the Selenium driver:
        self.opt = Options()
        self.path = Service('c:\\users\\chromedriver.exe')        
        self.selenium_arguments = [f"user-agent= {self.headers}", "window-size=1400,900", '--silent', '--no-sandbox', 'disable-notifications', '--disable-dev-shm-usage', '--disable-gpu']

        # Running the Selenium driver:
        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)
        
        
    def hamrobazar_automation(self):       
        self.opt.headless = True

        driver = webdriver.Chrome(service=self.path, options=self.opt) 
        driver.maximize_window()
        driver.get(self.url)     
       
        body_page = WebDriverWait(driver, 10).until((EC.presence_of_element_located((By.TAG_NAME, 'body'))))
        
        product_links = WebDriverWait(driver, 10).until((EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-redirect'))))
        # For price:
        listed_prices = WebDriverWait(driver, 10).until((EC.presence_of_all_elements_located((By.CLASS_NAME, 'price--main'))))
        
        all_product_links = [WebDriverWait(links, 10).until((EC.presence_of_element_located((By.TAG_NAME, 'a')))).get_attribute('href') for links in product_links]
        all_product_names = [WebDriverWait(names, 10).until((EC.presence_of_element_located((By.TAG_NAME, 'a')))).text.strip() for names in product_links]
        all_product_prices = [price.text.strip() for price in listed_prices]

       
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:                                 
            try:                
                driver.execute_script("window.scrollTo(5, document.body.scrollHeight);")
                driver.implicitly_wait(10)
                sleep(2)
                product_links1 = WebDriverWait(driver, 10).until((EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-redirect'))))
                # For price:
                listed_prices1 = WebDriverWait(driver, 10).until((EC.presence_of_all_elements_located((By.CLASS_NAME, 'price--main'))))
                
                for link in product_links1:
                    links_hyper = WebDriverWait(link, 10).until((EC.presence_of_element_located((By.TAG_NAME, 'a')))).get_attribute('href')
                    all_product_links.append(links_hyper)
                    product_names = WebDriverWait(link, 10).until((EC.presence_of_element_located((By.TAG_NAME, 'a')))).text.strip()
                    all_product_names.append(product_names)
                    print(product_names)

                
                for prices in listed_prices1:
                    all_product_prices.append(prices.text.strip())

                    
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            except:
                break
        
        sleep(2)
        driver.quit()
        
        return all_product_names, all_product_prices, all_product_links
    

    def category_name(self):
        self.opt.headless = True
        driver = webdriver.Chrome(service=self.path, options=self.opt)

        driver.maximize_window()
        driver.get(self.url)
        
        print("Scraping category.\n-------------------------------- ")
        WebDriverWait(driver, 10).until((EC.presence_of_element_located((By.TAG_NAME, 'body'))))
        name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'search--titles'))).text.strip().replace("Category : ", "")

        driver.quit()
        return name
