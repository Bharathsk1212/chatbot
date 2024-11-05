from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import ast

# Base URL for constructing full URLs from relative paths
base_url = "https://uk.webuy.com"

# The main category URL for Phones (as you mentioned)
phones_url = "https://uk.webuy.com/supercat?superCatId=4&superCatName=Phones"

# Function to update faqData.py with new FAQs or subcategory data
def update_faq_data(new_faqs):
    """Update the faqData.py with new FAQs."""
    faq_file = 'faqData.py'  # Path to the faqData.py file

    # Step 1: Read the existing FAQs from faqData.py
    try:
        with open(faq_file, 'r') as file:
            content = file.read()
            # Extract the current dictionary (assuming it's defined as 'faqs = {...}')
            existing_faqs_dict = ast.literal_eval(content.split('=')[1].strip())
    except Exception as e:
        print(f"Error reading {faq_file}: {e}")
        return

    # Step 2: Update the dictionary with new FAQs (e.g., new phones data)
    existing_faqs_dict.update(new_faqs)

    # Step 3: Write the updated dictionary back to faqData.py
    try:
        with open(faq_file, 'w') as file:
            file.write('faqs = {\n')
            for question, answer in existing_faqs_dict.items():
                # Escape quotes in the answers to ensure proper formatting in Python
                escaped_answer = answer.replace('"', '\\"')
                file.write(f'    "{question}": "{escaped_answer}",\n')
            file.write('}\n')
        print("FAQs updated successfully.")
    except Exception as e:
        print(f"Error writing to {faq_file}: {e}")


# Function to set up the Selenium WebDriver
def setup_selenium_driver():
    """Set up the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless mode (no browser UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # For Linux-based systems

    # Initialize the WebDriver (make sure chromedriver is in your PATH or specify the path)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# Function to fetch page content using Selenium
def get_page_content(url, driver):
    """Fetch the page content using Selenium."""
    driver.get(url)

    # Wait until the specific element (subcategories) is loaded on the page
    try:
        # Waiting for a specific element (change the By selector based on what you're scraping)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.cx-image-card-title'))
        )
        page_source = driver.page_source
        return BeautifulSoup(page_source, 'html.parser')
    except Exception as e:
        print(f"Error waiting for page to load: {e}")
        return None


# Function to extract phones data from the page
def extract_phones_data(soup):
    """Extract relevant data from the Phones category page."""
    phones_data = {}

    if soup:
        # Extract subcategories under Phones (Smartphones, Featured Phones, etc.)
        phone_links = soup.find_all('a', href=True)

        # Find links related to subcategories like Smartphones, Featured Phones, etc.
        for link in phone_links:
            href = link['href']
            category_name = link.get_text(strip=True).lower()  # Extract the text and make it lowercase

            # Skip empty category names or invalid links
            if not category_name:
                continue  # Skip if the name is empty
            if 'search?productLineId' in href:
                full_url = base_url + href  # Create full URL for each subcategory
                phones_data[category_name] = full_url

    return phones_data


# Main function to get the Phones category data and update faqData.py
def get_category_data():
    """Fetch and extract data for the Phones category using Selenium."""
    print(f"Fetching data from {phones_url}...")

    # Setup the Selenium WebDriver
    driver = setup_selenium_driver()

    # Get the page content using Selenium
    soup = get_page_content(phones_url, driver)

    # Close the WebDriver after scraping
    driver.quit()

    # Extract data for phones and its subcategories
    phones_data = extract_phones_data(soup)

    # Print the extracted links for verification
    print("Phones Subcategories:", phones_data)

    # If data was extracted successfully, update faqData.py
    if phones_data:
        update_faq_data(phones_data)
        print(f"Extracted data: {phones_data}")
    else:
        print("No phones subcategories were found.")


# Fetch and update phones category data
get_category_data()
