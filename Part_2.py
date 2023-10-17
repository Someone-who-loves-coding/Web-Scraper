import csv
import requests
from bs4 import BeautifulSoup

# Function to scrape product details
def scrape_product_details(product_url):
    response = requests.get(product_url)
    product_details = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Description
        description = soup.find("div", {"id": "productDescription"})
        if description:
            product_details["Description"] = description.get_text()

        # ASIN
        asin = soup.find("th", text="ASIN")
        if asin:
            product_details["ASIN"] = asin.find_next("td").get_text()

        # Product Description
        product_description = soup.find("h1", {"id": "title"})
        if product_description:
            product_details["Product Description"] = product_description.get_text().strip()

        # Manufacturer
        manufacturer = soup.find("th", text="Manufacturer")
        if manufacturer:
            product_details["Manufacturer"] = manufacturer.find_next("td").get_text()

    return product_details

# Load the list of Product URLs obtained in Part 1
product_urls = [
    "https://www.amazon.in/dp/ASIN1",
    "https://www.amazon.in/dp/ASIN2",
    # Add more URLs as needed
]

# Scrape product details
product_details_data = []
for product_url in product_urls:
    product_details = scrape_product_details(product_url)
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
