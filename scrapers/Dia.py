import requests
import random

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from constants.constants import DIA_DATA, DIA_ERROR, DIA_PRICE, DIA_URL
from headers.headers import PROXIES, USER_AGENTS

tqdm.pandas()


class Dia:
  def __init__(self):

    self.diaDf = pd.read_json(DIA_DATA)


  def headers (self):
    return {
      'authority': 'www.dia.es',
      'cache-control': 'max-age=0',
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'sec-ch-ua-mobile': '?0',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'none',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-user': '?1',
      'User-agent': random.choice(USER_AGENTS),
      'http': random.choice(PROXIES).replace('\n', ''),
      'sec-fetch-dest': 'document',
      'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
      'cookie': 'criteoId=1629489725335; __dia_lng__=es; anonymous-consents=%5B%5D; AWSELB=998FD55D14F30D48851F0B57EB8F24C2F5537F615702DE554E6F4F82814CC80F3A2F14A17798097F64E42668520B95B3123E9DD0B382E8DD9A97BAF14942AC0EB28D96F36F; visid_incap_1848948=GIPkgsoHTmOYYKdbPCMGnToKIGEAAAAAQUIPAAAAAABN15L247O0IBBbdbVnlL5K; nlbi_1848948=xutnd8hbUQMijHB3H+WDtAAAAADnCW5WgMF6+8j29avV6KMk; bsUl=0; OptanonAlertBoxClosed=2021-08-20T20:02:12.264Z; brainsins_token=BS-8625485410-1; bsFromRefer=; bsCoId=3629489732100; _qc.sid=Kaz8pZXBjN2arEzNNIPjPejg; incap_ses_505_1848948=FsaLdMTy8moq5orRSR8CB7VaIWEAAAAAcrtUrGA8M2gR6jrxawn8xA==; JSESSIONID=7A70518B89655C809E3BEBFDF242D2B6.app12; OptanonConsent=isIABGlobal=false&datestamp=Sat+Aug+21+2021+20%3A57%3A55+GMT%2B0100+(hora+de+verano+de+Europa+occidental)&version=6.8.0&hosts=&consentId=33462296-d7f6-409e-ab71-93248535a919&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0003%3A1%2CC0002%3A1&geolocation=ES%3BCN&AwaitingReconsent=false',
    }
  def params (self, product):
    return (
      ('q', f'{product}:relevance'),
      ('text', f'{product}page=1'),
    )
  def priceList (self, productSoup):
    
    priceContainer = productSoup.find_all('p', class_='price')
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
      
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']

      try: 
        page = requests.get(DIA_URL, headers=self.headers(), params=self.params(name))
        priceList = self.priceList(BeautifulSoup(page.content, 'html.parser'))

        if priceList:
          priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': self.getAverage(priceList)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
      except ValueError:
        print("Response content is not valid Json")
        errorDf = errorDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
        pass


    priceDf.to_csv(DIA_PRICE, index=False)
    errorDf.to_csv(DIA_ERROR, index=False)
