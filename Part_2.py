import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import Part_1  # Import your list of URLs

def scrape_product_data(urls):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',  # Replace with your user-agent header
    }

    for url in urls:
        try:
            # Send an HTTP GET request to the URL with headers
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for request success

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the ASIN value on the page using the CSS selector
            asin = soup.select_one('[data-asin]')['data-asin']

            # Find all the <li> elements within the <ul>
            list_items = soup.select('div#detailBullets_feature_div ul li')

            # Loop through the list items and check for the one containing "Manufacturer"
            manufacturer = None
            for item in list_items:
                if "Manufacturer" in item.get_text():
                    manufacturer = item.find('span', class_='a-text-bold').find_next('span').get_text(strip=True)
                    break

            # Find the description from the page
            description_element = soup.find('span', id="productTitle", class_="a-size-large product-title-word-break")
            description = description_element.get_text(strip=True)

            # Create a DataFrame to store the data with specific column names
            data = pd.DataFrame({
                'ASIN': [asin],
                'Manufacturer': [manufacturer],
                'ProductDescription': [description]
            })

            # Export the data to a CSV file with specific column names
            data.to_csv('amazon_data.csv', mode='a', header=False, index=False, encoding='utf-8')

            print(f'Data from URL {url} has been scraped and saved to amazon_data.csv')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from URL {url}: {e}")
        except Exception as e:
            print(f"Error processing the page from URL {url}: {e}")

# List of URLs to scrape from Part_1
url_list = [product["Product URL"] for product in Part_1.product_data]  # Assuming this is your list of URLs

# Call the function to scrape data from the list of URLs
scrape_product_data(url_list)
