import argparse
import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# Create the output folder if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")

parser = argparse.ArgumentParser(description="Search doctors on Doctoralia by location")
parser.add_argument("--query", "-q", "-query", "--q", type=str, nargs="+")
parser.add_argument("--location", "--l", "-l", "-location", type=str, nargs="+")

args = parser.parse_args()

query_args = args.query
query = " ".join(query_args)

location_args = args.location

location = " ".join(location_args)


print(location)
print(query)

csv_filename = f"output/urls.csv"

# Set up the Chrome browser driver
with webdriver.Chrome() as driver:
    # Navigate to the listing page
    url = f"https://www.doctoralia.com.mx/buscar?q={query}&loc={location}"
    driver.get(url)

    try:
        # Store the URLs of the businesses
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            url_set = set()
            while True:
                    # wait for store cards to load
                    time.sleep(3)

                    # get store cards in feed
                    doctor_cards = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "dp-doctor-card")
                        )
                    )

                    for business in doctor_cards:
                        try:
                            url_element = business.find_element(By.CSS_SELECTOR, "a[href]")
                            url = url_element.get_attribute("href")
                            if url not in url_set:
                                writer.writerow([url])
                                url_set.add(url)
                        except Exception as e:
                            print("Error getting business url:", e)
                    
                    try:
                        next_button = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "a[data-test-id='pagination-next']")
                            )
                        )
                        next_page_url = next_button.get_attribute("href")
                        if next_page_url:
                            driver.get(next_page_url)
                        else:
                            print("No more pages found")
                            break
                    except TimeoutException:
                        print("No more pages found")
                        break

            print("Loop completed")
            print(f"Got a total of {len(url_set)} urls")
                    

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()
        exit()
