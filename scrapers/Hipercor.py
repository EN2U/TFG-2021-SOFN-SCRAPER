import requests
import random
import re

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


from headers.headers import PROXIES, USER_AGENTS

# hipercor da problemas con un user-agent randomizado xdimport requests


class Hipercor:
  def __init__ (self):
    self.hipercorDf = pd.read_json("./dataScraped/hipercor/parsedHipercor.json")

  
  def headers (self):
    print(random.choice(PROXIES).replace('\n', ''))
    return {
      'authority': 'www.hipercor.es',
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'sec-ch-ua-mobile': '?0',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
      'accept': '*/*',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'proxy': random.choice(PROXIES).replace('\n', ''),
      'sec-fetch-dest': 'empty',
      'referer': 'https://www.hipercor.es/supermercado/buscar/?term=chocolate&search=text',
      'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
      'cookie': 'store=hipercorStore; session_id=c6c5fc035f250fa1289ef951968f2bae73caa25baf3b7222b2eb5f61c581da3a; centre=NULL; cookiesPolicy=10001; bm_sz=5B1EDBDD30767035C6D5166E4AB9CCD7~YAAQjmwQAjX5cSV7AQAA739PaAwvQQVW7V+h0MUjXDG7o013g9nGaJFcwpjxvxlcZxtC1ZOWyUJhWLjLUfVN19TwWF67ZEyW5G4DKdSV/sMxp19g/45KXDfLa1T0gTPNvhEnMUOUCTJjcUX0zjqnGyiN4jm/9Grvs9gAKlH20lnAXEWSnGiofb7TgVHa+KUdciw3e21ZNbL9pSyEProLP6NNbhdKeVEMmjYwRYkdFy2y2nrUSuhI5gCUy0iF7ypb+YHEG3I74DEIWMC8vrkcY45L8CgUfa3WUi1n5yPu/KkTCL8R~3750198~3289395; locale=es; bm_mi=03A72E0A9CF698DABC43E7745BD14ADC~L+YZVecEXXdTpLsQIrVYnOArhS3//8OPXR+nrW856VQ+jXN2p8c8T+oYXJ5HdUNv8wFmoeXjOL11hSrd1m1Q73XMMf7e/feWrjZ6XPHiXq/3NGw/1FsrR3kBAOE3Il1MMyAQ7bmIzc50c83a9SSpLyZVkBe9n6Sl4tdps5xKDoEnaCg55dEMtB4CMuQpgTTMxCIcAtXUf9k4idPiTwwgzAFnzrjP4fm8DwwCxiAio6E+JCj/TBmBd4IvftLB0BKn; _abck=15DDA598166564D6C926733DD5BB0899~0~YAAQrjRoaKRSQWh7AQAA3MuPaAZM3ygA0fC+2t8DDakQM9MnheJjO58v5ITWcX7tHmyqGA1AwaLVTiiGWX+iBBHQwof9vX3CcyLXf/Gh1iavH571uVqJJDsWZfjIOu5DZiYildDnkGEx5ZiJktIZhvBRiCLggOcxjoCSEza9JYHQPPMYVIpy+2+SBnwEVVRMSKrmWBA715JWK1esX28bgQVLjPiCkv1C9TakkzUwsGH/zhwnQrYX7S56NRxoAhmQ8eKhD5jewvLkONQVLFf1xBZZfLiiY/YrNFTOBTmi7KWGXhKD0V7/kRsKrh00w6UcXwSq39iPwUe92ybnJvkjMDkEog5mrjUndMgsdtBlVZkr4n+qWTikUBC92f18mds4eSqFBJD3oSEdRtVIi1mbHBqnUllfq6pF~-1~-1~-1; ak_bmsc=54EAB1F31D0B44CF8AFA3F5BD03A502E~000000000000000000000000000000~YAAQrjRoaKVSQWh7AQAA3MuPaAzShp+MHNj5VnagGwsqVVyk8t9BnnaeQqVunQ7LAvjFg6MtuA3NGXWLygIwFS7wIh/c0EeNWS7MrB4Ve28HE9XlZben6blxsxYVOAEduE8730EH/wKUl6FOpwosAEZXNleubFblFTyINwpxUDHmPw/VONe2JRqkB4sFFHTlyxSJKH9LM2vQFYY1s6tj7niJ7e/pOrJhwunP1bKoTLGoO7Ws5Y02Pr/MxD0Fn84n5WqBDpsN23gIIjLi6UJb/350kbO16JwOxpiRLASyd0WAz8wfsnCjlP3ZMJnUlXtNs8GWgSUwt8LjbcTqaJBdqk5opX/FCWWWbRGIZtV2mt8B2Ig7AyM/Q6e45jWLeBbsCQbviPHIIiK2AUqMZBdznDunsq1InHLh1w+UD6hzWx+DNYlkf+3NTGa71id7opaApvxx4ASLLs5L8mNm/orUI8nclr4DiN/s7QjP29Mz0dvekGL1GvCA9gM3Pw==; ADRUM_BT=R:71|i:1595648|g:518eb9d0-ab4a-45ec-889a-1e8ea7815ca5411|e:69|n:ElCorteIngles_21ebfd29-5f f5-438e-8f46-bd65ec7500ec',
}
  def priceList (self, productSoup):

    priceContainer = productSoup.find_all('div', class_='prices-price _current')
    return [ float(e.text.replace('\n', '').replace(' ', '').replace('€', '').replace(',', '.')) for e in priceContainer ]


  def getAverage (self, priceList):
    return sum(priceList) / len(priceList)

  def initializeScraper (self):
    priceDf = pd.DataFrame()
    errorDf = pd.DataFrame()
    for index, row in tqdm(self.hipercorDf.iterrows(), total=self.hipercorDf.shape[0]):
      
      headers = self.headers()
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']

      try: 
        
        page = requests.get(f'https://www.hipercor.es/supermercado/buscar/?term={name}&search=text', headers=headers)
        priceList = self.priceList(BeautifulSoup(page.content, 'html.parser'))

        if priceList:
          priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': self.getAverage(priceList)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
      except ValueError:
        print("Response content is not valid Json")
        errorDf = errorDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
        pass

    priceDf.to_csv("./dataScraped/hipercor/hipercorPrices.csv", index=False)
    errorDf.to_csv("./dataScraped/errorHipercorPrices.csv", index=False)