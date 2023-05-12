from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
import csv
import os
import re

# Create the output folder if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")


csv_urls_filename = f"output/urls.csv"

csv_filename = "output/data.csv"

with webdriver.Chrome() as driver:
    try:
        with open(csv_urls_filename, "r") as csvfile:
            urls = csv.reader(csvfile)
            with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "name",
                        "specialization",
                        "rating",
                        "reviews",
                        "phone_number",
                        "consultation_price"
                    ]
                )
                for row in urls:
                    url = row[0]
                    if url and isinstance(url, str):
                        driver.get(url)

                        time.sleep(3)

                        try:
                            name = (
                                WebDriverWait(driver, 2)
                                .until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-id='profile-fullname-wrapper']")))
                                .text
                            )

                        except Exception as e:
                            print("no name found")
                            name = ""

                        try:
                            specialization = (
                                WebDriverWait(driver, 2)
                                .until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-test-id='doctor-specializations']")))
                                .text
                            )

                        except Exception as e:
                            print("no specialization found")
                            specialization = ""
                        
                        try:
                            rating_element = (
                                WebDriverWait(driver, 2)
                                .until(EC.presence_of_element_located((By.CLASS_NAME, "rating")))
                            )
                            rating = rating_element.get_attribute("data-score")
                             

                        except Exception as e:
                            print("no rating found")
                            rating = ""

                        try:
                            reviews = (
                                WebDriverWait(driver, 2)
                                .until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-switch-tab='profile-reviews']")))
                                .text
                            )

                            reviews = int(re.search(r'\d+', reviews).group())
                             

                        except Exception as e:
                            print("no reviews found")
                            reviews = ""



                        try:
                            phone_number_element = WebDriverWait(driver, 2).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-patient-app-event-name='dp-call-phone']"))
                            )
                            phone_number = phone_number_element.get_attribute("href").replace("tel:", "")

                        except Exception as e:
                            print("no phone found")
                            phone_number = ""

                        try:
                            # Find the element containing the price
                            price_element = WebDriverWait(driver, 2).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-id='service-price']"))
                            )

                            # Get the price text
                            price_text = price_element.text.strip()

                            # Extract the price value using a regular expression
                            price = re.search(r'\$([\d,]+)', price_text)
                            if price:
                                consultation_price = price.group(1).replace(',', '')
                            else:
                                consultation_price = ""

                            print(consultation_price)
                        except Exception as e:
                            print("no service price found")
                            consultation_price = ""

                        if name:
                            writer = csv.writer(csvfile)
                            writer.writerow([name, specialization, rating, reviews, phone_number, consultation_price])
                            
                    else:
                        print(f"Invalid URL format: {url}")

    except Exception as e:
            print("Error getting data")

    finally:
        # Close the driver
        driver.quit()
        exit()
