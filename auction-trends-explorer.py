import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Define the URL and headers
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_auction_data(page_number):
    url = base_url.format(page_number)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('article', class_='product_pod')
        data = []
        for item in items:
            title = item.h3.a['title']
            price = item.find('p', class_='price_color').text.strip()
            data.append({'title': title, 'price': price})
        return data
    else:
        print('Failed to retrieve data')
        return []

# Scrape multiple pages
all_auction_data = []
for page in range(1, 6):
    all_auction_data.extend(scrape_auction_data(page))
    time.sleep(1)

# Convert to DataFrame
auction_df = pd.DataFrame(all_auction_data)
auction_df['price'] = auction_df['price'].str.replace('£', '').astype(float)
print(auction_df.head())

# Save the data to a CSV file
auction_df.to_csv('auction_data.csv', index=False)

# Data Analysis
auction_data = pd.read_csv('auction_data.csv')
auction_data['price'] = auction_data['price'].astype(float)
average_price_by_item = auction_data.groupby('title')['price'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=average_price_by_item.values, y=average_price_by_item.index)
plt.title('Average Price by Auction Item')
plt.xlabel('Average Price (£)')
plt.ylabel('Item')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(auction_data['price'], bins=20, kde=True, color='blue')
plt.title('Distribution of Auction Item Prices')
plt.xlabel('Price (£)')
plt.ylabel('Frequency')
plt.show()
