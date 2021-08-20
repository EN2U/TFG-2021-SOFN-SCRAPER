import requests
import random

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from headers.headers import PROXIES, USER_AGENTS

tqdm.pandas()


class Alcampo:
  def __init__(self, df):
    self.alcampoDf = df


  def headers (self):
    return {
      'Host': 'www.alcampo.es',
      'Connection': 'keep-alive',
      'language': 'ca-ES',
      'User-agent': random.choice(USER_AGENTS),
      'https': random.choice(PROXIES).replace('\n', ''),
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'Accept': 'application/json, text/plain, */*'
    }

  def priceList (self, productSoup):
    
    priceContainer = productSoup.find_all('span', class_='price')
    priceContainer = priceContainer[2:len(priceContainer)]
    priceList = list()
    
    for item in priceContainer:
        priceList.append(item.text)

    priceList = [x.replace('\n', '').replace(' ', '') for x in priceList]
    
    return priceList
  
  def getAverage (self, priceList):
    x = float(0.00)
    avgPrice = float(0.00)
    for price in priceList:
      x = float(price.split("€")[0].replace(",", "."))
      avgPrice = avgPrice + x
    return avgPrice / len(priceList)
  
  def initializeScraper (self):
    priceDf = pd.DataFrame()
    for index, row in tqdm(self.alcampoDf.iterrows(), total=self.alcampoDf.shape[0]):
      
      headers = self.headers()
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']
      page = requests.get(f'https://www.alcampo.es/compra-online/search?q={name}%3Arelevance&text={name}page=1', headers=headers)

      productSoup = BeautifulSoup(page.content, 'html.parser')
      priceList = self.priceList(productSoup)

      if priceList:
        priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': self.getAverage(priceList)}, ignore_index=True, verify_integrity=False)
      else:
        priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
        
    priceDf.to_csv("./dataScraped/alcampo/alcampoPrices.csv", index=False)

      