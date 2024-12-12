# scraping and analyzing the suumo rental pricing (Odawara)

from bs4 import BeautifulSoup as bs
import requests
from logger.logger import log

def scrape(location):
    # variables
    prefecture = location["prefecture"]
    city = location["city"]
    base_url = f"https://www.homes.co.jp/chintai/{prefecture}/{city}-city/list/?page="
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    prices = []
    for i in range(1, 2):
        try:
            response = requests.get(f"{base_url}{i}", headers=headers)
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            html_content = response.text
            
            # log(html_content)
            
            soup = bs(html_content, 'html.parser')
            # Find all parent elements with class
            elements = soup.find_all('span', class_='priceLabel')
            # Extract child elements with the specific class within the parent
            
            for element in elements:
                price = element.find('span', class_='num')
                price = price.text
                if price:
                    price = float(price) * 10000
                    prices.append(price)

            # Calculate the frequency of each price
            frequency = {}

            for price in prices:
                price = str(round(price, -3))
                frequency[price] = frequency.get(price, 0) + 1
                
            frequency = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
            
            if len(prices) == 0:
                avg = 0
            else:
                avg = int(sum(prices) / len(prices))
            return {"listings": len(prices), "average price": avg, "frequency": frequency}
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {i}: {e}")
            return "Failed"
            

            
    

    
            
