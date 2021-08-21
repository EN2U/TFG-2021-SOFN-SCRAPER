import requests
import random

import pandas as pd
from constants.constants import ALCAMPO_DATA, AUCHAN_DATA, ALCAMPO_URL, ALCAMPO_PRICE, ALCAMPO_ERROR

from tqdm import tqdm
from bs4 import BeautifulSoup

from headers.headers import PROXIES, USER_AGENTS

tqdm.pandas()


class Alcampo:
  def __init__(self):

    df1 = pd.read_json(ALCAMPO_DATA)
    df2 = pd.read_json(AUCHAN_DATA)
    self.alcampoDf = pd.concat([df1, df2])

  def cookies (self):
    return {
      'JSESSIONID2': '4B2D6A15ECF269F82551DE0585743511.pro-ftp',
      'cookieLanguageHybris': 'es',
      'cp': '28029',
      'deliveryMode': 'PICKUP_DELIVERY_MODE',
      'shopId': '005',
      'precode': '',
      'localizedAs': 'anonymous',
      'selectionMode': 'selectedByUser',
      'GUEST_LANGUAGE_ID': 'es_ES',
      'COOKIE_SUPPORT': 'true',
      'dtCookie': 'CE3FB90247E0402558C148EFED3D9C88',
      'YOMe1hXPsDqscWomlSmem06yAMon28t8Vfv7k7W8mw__': 'v1B+CGSQ__92Z',
      'cookie_consent_user_accepted': 'true',
      'alcampoSpainStoreUid-cart': '1a920ffc-babe-4cc7-afa4-5fbf6af5191b',
      'chatbot_id': '4B2D6A15ECF269F82551DE0585743511',
      'cookie_consent_level': '%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%2C%22tracking%22%3Atrue%2C%22targeting%22%3Atrue%7D',
    }

  def headers (self):
    return {
      'authority': 'www.alcampo.es',
      'cache-control': 'max-age=0',
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'sec-ch-ua-mobile': '?0',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-user': '?1',
      'sec-fetch-dest': 'document',
        'User-agent': random.choice(USER_AGENTS),
      'https': random.choice(PROXIES).replace('\n', ''),
      'referer': 'https://www.alcampo.es/compra-online/search?q={name}%3Arelevance&text={name}page=1',
      'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
    }

  def params (self, product):
    return (
      ('department', ''),
      ('text', product),
    )

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

    for index, row in tqdm(self.alcampoDf.iterrows(), total=self.alcampoDf.shape[0]):
      
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']

      try: 
        page =  requests.get(ALCAMPO_URL, headers=self.headers(), params=self.params(name), cookies=self.cookies())

        priceList = self.priceList(BeautifulSoup(page.content, 'html.parser'))

        if priceList:
          priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': self.getAverage(priceList)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
      
      except ValueError:
        print("Response content is not valid Json")
        errorDf = errorDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
        pass

    priceDf.to_csv(ALCAMPO_PRICE, index=False)
    errorDf.to_csv(ALCAMPO_ERROR, index=False)
