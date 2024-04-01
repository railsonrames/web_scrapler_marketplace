import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def scrape_facebook_marketplace(username, password):
    # Path to the WebDriver executable (change this to the location of your WebDriver)
    webdriver_path = '/chromedriver_mac64'

    # Create a new instance of the Chrome WebDriver
    driver = webdriver.Chrome(executable_path=webdriver_path)

    # URL of the Facebook Marketplace
    url = 'https://www.facebook.com/marketplace'

    # Open the URL in the browser
    driver.get(url)

    # Wait for the page to load (adjust the sleep duration as needed)
    time.sleep(5)

    # Log in to Facebook
    login_button = driver.find_element_by_xpath("//a[@data-testid='cookie-policy-banner-accept']")
    login_button.click()
    login_button = driver.find_element_by_xpath("//a[@data-testid='login_button']")
    login_button.click()
    time.sleep(2)
    username_field = driver.find_element_by_id("email")
    username_field.send_keys(username)
    password_field = driver.find_element_by_id("pass")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    # Get the page source after JavaScript has rendered
    page_source = driver.page_source

    # Parse the HTML content of the page
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the listings on the page
    listings = soup.find_all('div', class_='nc684nl6')

    # Extract information from each listing
    for listing in listings:
        # Example: Extract title and price
        title = listing.find('span', class_='d2edcug0').text.strip()
        price = listing.find('span', class_='a8c37x1j').text.strip()

        # Print the extracted information (you can modify this to save to a file or database)
        print(f'Title: {title}, Price: {price}')

    # Close the WebDriver
    driver.quit()

# Replace 'your_username' and 'your_password' with your actual Facebook credentials
scrape_facebook_marketplace('railson@msn.com', 'Brasil12*')
