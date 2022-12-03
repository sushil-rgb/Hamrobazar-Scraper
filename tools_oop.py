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


# Get random user-agent for scraping:
def get_user_agent():
    with open('user-agents.txt') as f:
        ua_strings = f.read().split("\n")
    return random.choice(ua_strings)


# This class extracts only products' links, name and prices from the main category url:
class HamrobazarScraper:
    def __init__(self, url):
        self.headers = {'User-Agent': get_user_agent()}
        self.url = url
        self.req = requests.get(url, headers=self.headers)

        # Setting up the Selenium driver:
        self.opt = Options()
        self.path = Service('c:\\users\\chromedriver.exe')
        self.selenium_arguments = [f"user-agent= {self.headers}", "window-size=1400,900", '--silent', '--no-sandbox',
                                   'disable-notifications', '--disable-dev-shm-usage', '--disable-gpu']

        # Running the Selenium driver:
        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Mimicking as a client while making a request to server:
        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)

    def hamrobazar_automation(self, interval):
        self.opt.headless = True
        driver = webdriver.Chrome(service=self.path, options=self.opt)
        driver.maximize_window()
        driver.get(self.url)

        body_page = WebDriverWait(driver, 10).until(
            (EC.presence_of_element_located((By.TAG_NAME, 'body'))))

        # For product links:
        product_links = WebDriverWait(driver, 10).until(
            (EC.visibility_of_all_elements_located((By.CLASS_NAME, 'product-redirect'))))
        # For price:
        listed_prices = WebDriverWait(driver, 10).until(
            (EC.visibility_of_all_elements_located((By.CLASS_NAME, 'price--main'))))

        # Storing all the scraped links, names and price to a list:
        all_product_links = [
            WebDriverWait(links, 10).until(
                (EC.visibility_of_element_located((By.TAG_NAME, 'a')))).get_attribute('href')
            for links in product_links]
        all_product_names = [
            WebDriverWait(names, 10).until((EC.visibility_of_element_located((By.TAG_NAME, 'a')))).text.strip() for
            names in product_links]
        all_product_prices = [price.text.strip() for price in listed_prices]

        # Get scroll height after first time page load:
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            try:
                # Scroll down to bottom:
                driver.execute_script(
                    "window.scrollTo(3, document.body.scrollHeight);")
                # Wait to load page:
                sleep(interval)
                product_links1 = WebDriverWait(driver, 10).until(
                    (EC.visibility_of_all_elements_located((By.CLASS_NAME, 'product-redirect'))))
                # For price:
                listed_prices1 = WebDriverWait(driver, 10).until(
                    (EC.visibility_of_all_elements_located((By.CLASS_NAME, 'price--main'))))

                # Again looping and appending to the existing variable and lists above:
                for link in product_links1:
                    links_hyper = WebDriverWait(link, 10).until(
                        (EC.visibility_of_element_located((By.TAG_NAME, 'a')))).get_attribute('href')
                    all_product_links.append(links_hyper)
                    product_names = WebDriverWait(link, 10).until(
                        (EC.visibility_of_element_located((By.TAG_NAME, 'a')))).text.strip()
                    all_product_names.append(product_names)
                    print(product_names)

                for prices in listed_prices1:
                    all_product_prices.append(prices.text.strip())

                # Calculate new scroll height and compare with last scroll height:
                new_height = driver.execute_script(
                    "return document.body.scrollHeight")
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

        WebDriverWait(driver, 10).until(
            (EC.presence_of_element_located((By.TAG_NAME, 'body'))))
        name = WebDriverWait(driver, 10).until((EC.presence_of_element_located(
            (By.CLASS_NAME, 'search--titles')))).text.strip().replace("Category : ", "")

        driver.quit()
        return name


# This class extracts the products' name, seller info, prices and so on from individual links:
class Hamrobazaar:
    def __init__(self, url):
        self.headers = {'User-Agent': get_user_agent()}
        self.url = url
        self.req = requests.get(url, headers=self.headers)

        # Setting up the Selenium driver:
        self.opt = Options()
        self.path = Service('c:\\users\\chromedriver.exe')
        self.selenium_arguments = [f"user-agent= {self.headers}", "window-size=1400,900", '--silent', '--no-sandbox',
                                   'disable-notifications', '--disable-dev-shm-usage', '--disable-gpu']

        # Running the Selenium driver:
        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Mimicking as a client while making a request to server:
        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)

        self.opt.headless = True
        self.driver = webdriver.Chrome(service=self.path, options=self.opt)
        self.driver.maximize_window()
        self.driver.get(self.url)

    def product_name(self):
        try:
            name = WebDriverWait(self.driver, 10).until(
                (EC.visibility_of_element_located((By.CLASS_NAME, 'title--relative')))).text.strip()
            sleep(2)
            self.driver.quit()
            return name
        except TimeoutException:
            sleep(2)
            self.driver.quit()

    def seller_name(self):
        try:
            s_name = self.driver.find_element(By.CLASS_NAME, 'seller__name--inner').find_element(By.TAG_NAME,
                                                                                                 'a').find_element(
                By.TAG_NAME, 'span').text.strip()
            sleep(2)
            self.driver.quit()

            return s_name
        except TimeoutException:
            sleep(2)
            self.driver.quit()

            return s_name

    def seller_contact(self):
        try:
            contact = self.driver.find_element(By.CLASS_NAME, 'seller__address').find_element(By.TAG_NAME,
                                                                                              'span').text.strip()
            sleep(2)
            self.driver.quit()

            return contact
        except NoSuchElementException:
            contact = "Not available"
            sleep(2)
            self.driver.quit()

            return contact

    def seller_link(self):
        try:
            link = self.driver.find_element(By.CLASS_NAME, 'seller__name--inner').find_element(By.TAG_NAME,
                                                                                               'a').get_attribute(
                'href')
            sleep(2)
            self.driver.quit()

            return link
        except NoSuchElementException:
            link = "Not available"
            sleep(2)
            self.driver.quit()

            return link

    def product_condition(self):
        try:
            condition = self.driver.find_element(By.XPATH,
                                                 '//*[@id="hb__root"]/div/main/div/aside[1]/div/div[1]/label').text.strip()
            sleep(2)
            self.driver.quit()

            return condition
        except NoSuchElementException:
            condition = "N/A"
            sleep(2)
            self.driver.quit()
            return condition
