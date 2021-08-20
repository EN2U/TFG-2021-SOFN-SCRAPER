import requests
import pandas as pd

from tqdm import tqdm
from bs4 import BeautifulSoup
import random
from headers.headers import PROXIES, USER_AGENTS



tqdm.pandas()

def initializeHeader ():
  user_agent = random.choice(USER_AGENTS)
  proxy = random.choice(PROXIES)
  print (proxy)
  return {
    'Host': 'www.alcampo.es',
    'Connection': 'keep-alive',
    'language': 'ca-ES',
    'User-agent': user_agent,
    'https': 'http://121.69.37.238:8118',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*'
  }

def initializePriceList (productSoup):
    
    priceContainer = productSoup.find_all('span', class_='price')
    priceContainer = priceContainer[2:len(priceContainer)]
    priceList = list()
    
    for item in priceContainer:
        priceList.append(item.text)

    priceList = [x.replace('\n', '').replace(' ', '') for x in priceList]
    
    return priceList


def initializeProductList (productSoup):
    
    productsContainer = productSoup.find_all('div', class_='productName truncate')
    productList = list()
    
    for item in productsContainer:
        productList.append(item.text)

    return productList

def getFilters ():
    a = input("Enter product:")
    b = 1
    
    return a, b

def getAverage (priceList):
  x = float(0.00)
  avgPrice = float(0.00)
  for price in priceList:
    x = float(price.split("€")[0].replace(",", "."))
    avgPrice = avgPrice + x
  return avgPrice / len(priceList)

def alcampoScrap (df):
    priceDf = pd.DataFrame()
    dictionary = {}
    size = 0
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        
        header = initializeHeader()

        if row['product_name_es']:
          name = row['product_name_es']
          page = requests.get(f'https://www.alcampo.es/compra-online/search?q={name}%3Arelevance&text={name}page=1', headers=header)

        else:
          name = row['product_name']
          page = requests.get(f'https://www.alcampo.es/compra-online/search?q={name}%3Arelevance&text={name}page=1', headers=header)

        print (page)
        productSoup = BeautifulSoup(page.content, 'html.parser')
        productList = initializeProductList(productSoup)
        priceList = initializePriceList(productSoup)
        if priceList:
          priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': getAverage(priceList)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
        if size > 2:
          break
    priceDf.to_csv("alcampoPrices.csv", index=False)

    
if __name__ == "__main__":
    df = pd.read_json("./parsedAlcampo.json")
    alcampoScrap(df)

    """     chunks = pd.read_json('data.json', lines=True, chunksize = 10000)
    for chunk in chunks:
        print(chunk)
        break 
        
     with open('data') as json_file:      
        data = json_file.readlines()
    # this line below may take at least 8-10 minutes of processing for 4-5 million rows. It converts all strings in list to actual json objects. 
        data = list(map(json.loads, data)) 
    pd.DataFrame(data)
    """