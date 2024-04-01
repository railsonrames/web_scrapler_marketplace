import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def scrape_facebook_marketplace(target_term: str, target_location: str):
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    url = 'https://www.facebook.com/marketplace'
    driver.get(url)

    time.sleep(2)
    cookies_text_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Permitir todos os cookies')]")
    cookies_button_element = cookies_text_element.find_element(By.XPATH,  "../../../../../../..")
    cookies_button_element.click()
    time.sleep(2)
    close_login_element = driver.find_element(By.XPATH, "//div[@aria-label='Fechar']")
    close_login_element.click()
    time.sleep(1)
    close_zipcode_element = driver.find_element(By.XPATH, "//div[@aria-label='Fechar']")
    close_zipcode_element.click()
    time.sleep(2)
    login_block_element = driver.find_element(By.XPATH, "//div[@data-nosnippet='']")
    driver.execute_script("arguments[0].remove();", login_block_element)
    time.sleep(2)
    location_icon_element = driver.find_element(By.XPATH, "//span[contains(text(), 'San Francisco')]")
    location_icon_element.click()
    time.sleep(1)
    input_location_element = driver.find_element(By.XPATH, "//input[@aria-label='Localização']")
    time.sleep(1)
    input_location_element.clear()
    ActionChains(driver).send_keys_to_element(input_location_element, target_location).perform()
    time.sleep(1)
    city_dropdown_element = driver.find_element(By.XPATH, "//span[text()='Lisboa']")
    city_dropdown_element.click()
    submit_location_button = driver.find_element(By.XPATH, "//div[@aria-label='Aplicar']")
    submit_location_button.click()
    time.sleep(2)
    input_serch_term = driver.find_element(By.XPATH, "//input[@type='search']")
    input_serch_term.clear()
    ActionChains(driver).send_keys_to_element(input_serch_term, target_term).perform()
    input_serch_term.send_keys(Keys.RETURN)
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    listings_imgs = soup.find_all('img')
    listings_euro_sign = soup.find_all(' €')
    for listing in listings_imgs:
        title = listing.attrs['alt']
    for listgin in listings_euro_sign:
        price = listing
    price_tag = soup.find(text=re.compile(r'\b€\b'))
    price = re.search(r'(\d+(?:[.,]\d+)?)\s*€', price_tag).group(1)
    car_info = price_tag.find_next('span').get_text(strip=True)
    location = car_info.find_next('span').get_text(strip=True)
    print(f"Título: {car_info}\nLocalização: {location}\nPreço: {price}")
    time.sleep(20)
    driver.quit()

target_term = "Hyundai i20 2016"
target_location = "Lisboa, Portugal"
scrape_facebook_marketplace(target_term, target_location)