import csv
import requests
from bs4 import BeautifulSoup
import time

# Function to scrape product listings with proxy rotation
def scrape_product_listings(url, num_pages, proxy_list):
    all_product_data = []

    for page in range(1, num_pages + 1):
        proxy = proxy_list[page % len(proxy_list)]  # Rotate through proxy list
        page_url = f"{url}&page={page}"

        try:
            response = requests.get(page_url, proxies=proxy, timeout=10)

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

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from page {page}: {e}")
        except Exception as e:
            print(f"Error processing page {page}: {e}")

    return all_product_data

# Amazon URL for bags
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Number of pages to scrape (adjust as needed)
num_pages = 200

# List of rotating proxies (replace with your own proxy list)
proxy_list = [
    {"http": "http://154.58.202.47:1337"},
    {"http": "http://103.59.215.30:1080"},
    {"http": "http://117.212.92.228:5678"},
    {"http": "http://20.219.182.59:3129	"},
    # Add more proxy entries as needed
]

# Scrape product listings with proxy rotation
product_data = scrape_product_listings(url, num_pages, proxy_list)

# Save the data to a CSV file with UTF-8 encoding
with open("product_listings.csv", "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.DictWriter(csvfile, fieldnames=product_data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(product_data)

print("Product listings scraped and saved to product_listings.csv")
