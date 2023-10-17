import csv
import requests
from bs4 import BeautifulSoup
import time

# Function to scrape product listings
def scrape_product_listings(url, num_pages):
    all_product_data = []

    for page in range(1, num_pages + 1):
        page_url = f"{url}&page={page}"
        response = requests.get(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            product_divs = soup.find_all("div", class_="s-result-item")

            for div in product_divs:
                product_data = {
                    "Product URL": "",
                    "Product Name": "",
                    "Product Price": "",
                    "Rating": "",
                    "Number of Reviews": ""
                }

                # Product URL
                link = div.find("a", class_="a-link-normal s-no-outline")
                if link:
                    product_data["Product URL"] = "https://www.amazon.in" + link["href"]

                # Product Name
                name = div.find("span", class_="a-text-normal")
                if name:
                    product_data["Product Name"] = name.get_text()

                # Product Price
                price = div.find("span", class_="a-price")
                if price:
                    product_data["Product Price"] = price.get_text()

                # Rating
                rating = div.find("span", class_="a-icon-alt")
                if rating:
                    product_data["Rating"] = rating.get_text()

                # Number of Reviews
                reviews = div.find("span", class_="a-size-base")
                if reviews:
                    product_data["Number of Reviews"] = reviews.get_text()

                all_product_data.append(product_data)

            time.sleep(1)  # Respectful scraping by adding a delay

    return all_product_data

# Amazon URL for bags
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# to limit scraping to 20 pages
num_pages = 20

# Scrape product listings
product_data = scrape_product_listings(url, num_pages)

# Save the data to a CSV file with UTF-8 encoding
with open("product_listings.csv", "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.DictWriter(csvfile, fieldnames=product_data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(product_data)

print("Part 1: Product listings scraped and saved to product_listings.csv")
