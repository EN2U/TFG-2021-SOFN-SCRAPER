import requests
import json

import random

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from headers.headers import PROXIES, USER_AGENTS

tqdm.pandas()


class Mercadona:
  def __init__(self):

    self.mercadonaDf = pd.read_json("./dataScraped/mercadona/parsedMercadona.json")


  def headers (self):
    return {
      'Connection': 'keep-alive',
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'accept': 'application/json',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
      'content-type': 'application/x-www-form-urlencoded',
      'Origin': 'https://tienda.mercadona.es',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'Referer': 'https://tienda.mercadona.es/',
      'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
      'Content-Type': 'application/json',
      'User-agent': random.choice(USER_AGENTS),
      'http': random.choice(PROXIES).replace('\n', ''),
    }

  def payload (self, product):
    return json.dumps({
    "query": product,
    "clickAnalytics": "true",
    "analyticsTags": "['web']"
  })

  def priceList (self, productSoup):
    
    print (productSoup)
    priceContainer = productSoup.find_all('p', class_='product-price__unit-price subhead1-b')
    priceContainer = priceContainer[2:len(priceContainer)]
    priceList = list()
    
    for item in priceContainer:
        priceList.append(item.text)

    priceList = [x.replace('\n', '').replace(' ', '') for x in priceList]
    
    return priceList
  
  def getAverage (self, priceList):
    return sum(priceList) / len(priceList)
  
  def initializeScraper (self):
    priceDf = pd.DataFrame()
    errorDf = pd.DataFrame()

    for index, row in tqdm(self.mercadonaDf.iterrows(), total=self.mercadonaDf.shape[0]):
      
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']

      try: 
        page = requests.post('https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_vlc1_es/query?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser&x-algolia-application-id=7UZJKL1DJ0&x-algolia-api-key=9d8f2e39e90df472b4f2e559a116fe17', headers=self.headers(), data=self.payload(name)).json()

        if 'hits' in page:
          priceList = [ float(e['price_instructions']['unit_price']) for e in page['hits']]
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': self.getAverage(priceList) if priceList else float(0.00)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
      except ValueError:
        print("Response content is not valid Json")
        errorDf = errorDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
        pass

    priceDf.to_csv("./dataScraped/mercadona/mercadonaPrices.csv", index=False)
    errorDf.to_csv("./dataScraped/mercadona/errorMercadonaPrices.csv", index=False)
