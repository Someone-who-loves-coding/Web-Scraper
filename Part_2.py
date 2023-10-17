import csv
import requests
from bs4 import BeautifulSoup
import time

# Function to scrape product details with retry mechanism
def scrape_product_details_with_retry(product_url, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',  # Replace with a user-agent header
    }
    
    for retry in range(max_retries):
        try:
            response = requests.get(product_url, headers=headers)
            response.raise_for_status()  # Check for HTTP request errors

            product_details = {}

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Description
                description = soup.find("div", {"id": "productDescription"})
                if description:
                    product_details["Description"] = description.get_text()

                # ASIN
                asin = soup.find("th", string="ASIN")
                if asin:
                    product_details["ASIN"] = asin.find_next("td").get_text()

                # Product Description
                product_description = soup.find("h1", {"id": "title"})
                if product_description:
                    product_details["Product Description"] = product_description.get_text().strip()

                # Manufacturer
                manufacturer = soup.find("th", string="Manufacturer")
                if manufacturer:
                    product_details["Manufacturer"] = manufacturer.find_next("td").get_text()

            return product_details
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"Error while scraping {product_url} (Attempt {retry + 1}/{max_retries}): {e}")
            if retry < max_retries - 1:
                time.sleep(5)  # Wait for a while before retrying
    return None

# Load the list of Product URLs obtained in Part 1
product_urls = [
    "https://www.amazon.in/Dyazo-Resistant-Photographers-Compatible-Panasonic/dp/B0BWWD1QQQ?sbo=Tc8eqSFhUl4VwMzbE4fw%2Fw%3D%3D"
    # Add more URLs as needed
]

# Scrape product details
product_details_data = []
for product_url in product_urls:
    product_details = scrape_product_details_with_retry(product_url)
    if product_details:
        product_details_data.append(product_details)

# Check if product_details_data is not empty before writing to CSV
if product_details_data:
    with open("product_details.csv", "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=product_details_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(product_details_data)

    print("Part 2: Product details scraped and saved to product_details.csv")
else:
    print("Part 2: No product details to save")
