import requests
import random

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from headers.headers import PROXIES, USER_AGENTS

tqdm.pandas()


class Dia:
  def __init__(self):

    self.diaDf = pd.read_json("./dataScraped/dia/parsedDia.json")


  def headers (self):
    return {
      'Connection': 'keep-alive',
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'accept': 'application/json',
      'sec-ch-ua-mobile': '?0',
      'User-agent': random.choice(USER_AGENTS),
      'http': random.choice(PROXIES).replace('\n', ''),
      'content-type': 'application/x-www-form-urlencoded',
      'Origin': 'https://tienda.mercadona.es',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'Referer': 'https://tienda.mercadona.es/',
      'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
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
    errorDf = pd.DataFrame()

    for index, row in tqdm(self.diaDf.iterrows(), total=self.diaDf.shape[0]):
      
      headers = self.headers()
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']

      try: 
        page = requests.get(f'https://www.dia.es/compra-online/search?q={name}%3Arelevance&text={name}page=1', headers=headers)

        priceList = self.priceList(productSoup = BeautifulSoup(page.content, 'html.parser'))

        if priceList:
          priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': self.getAverage(priceList)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
      except ValueError:
        print("Response content is not valid Json")
        errorDf = errorDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
        pass

    priceDf.to_csv("./dataScraped/dia/diaPrices.csv", index=False)
    errorDf.to_csv("./dataScraped/dia/errorDiaPrices.csv", index=False)
