import requests
import random

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from headers.headers import PROXIES, USER_AGENTS

tqdm.pandas()


class Eroski:
  def __init__(self):

    self.alcampoDf = pd.read_json("./dataScraped/eroski/parsedEroski.json")

  def cookies (self):
    return {
      'supermarket.locale': 'es',
      'supermarket.direct_access': 'true',
      'supermarket.site': 'eroski',
      'supermarket.shop': '157',
      'supermarket.device_type': 'DESKTOP',
      'supermarket.cookies': '1',
      'supermarket.data_protection': '1',
      'supermarket.small_view': 'false',
      'JSESSIONID': '66D9AF49527FFEBFC9F56EFADA33BCCE.D3BB16AFCDB627BDE0AD39ACCDB63AF88DAA',
    }


  def headers (self):
    return {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'sec-ch-ua-mobile': '?0',
      'Upgrade-Insecure-Requests': '1',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document',
      'User-agent': random.choice(USER_AGENTS),
      'https': random.choice(PROXIES).replace('\n', ''),
      'Referer': 'https://supermercado.eroski.es/',
      'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    }

  def params (self):
    return (
      ('q', 'chocolate'),
      ('suggestionsFilter', 'false'),
    )

  def priceList (self, productSoup):
    
    priceContainer = productSoup.find_all('span', class_='price-offer-now')
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

    for index, row in tqdm(self.alcampoDf.iterrows(), total=self.alcampoDf.shape[0]):
      
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']

      try: 
        page = requests.get(f'https://supermercado.eroski.es/es/search/results/', headers=self.headers(), params=self.params(), cookies=self.cookies())

        priceList = self.priceList(productSoup = BeautifulSoup(page.content, 'html.parser'))

        if priceList:
          priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': self.getAverage(priceList)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
      except ValueError:
        print("Response content is not valid Json")
        errorDf = errorDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
        pass

    priceDf.to_csv("./dataScraped/eroski/eroskiPrices.csv", index=False)
    errorDf.to_csv("./dataScraped/eroski/errorEroskiPrices.csv", index=False)
