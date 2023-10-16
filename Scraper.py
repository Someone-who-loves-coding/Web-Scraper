from urllib.parse import urljoin
from  bs4 import BeautifulSoup
import requests

url = "https://www.amazon.in/s?k=bags&ref=sr_pg_1"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page = requests.get(url, headers=headers)

soup1 = BeautifulSoup(page.content, 'html.parser')
# Product_URL = soup1.find(id ="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
for item in soup1:
    print(urljoin(url, item['href']))

# soup2 = BeautifulSoup()
# soup3 = BeautifulSoup()
# soup4 = BeautifulSoup()
# soup5 = BeautifulSoup()
