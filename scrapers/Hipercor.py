import requests
import random

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from constants.constants import CORTE_INGLES_DATA, HIPERCOR_DATA, HIPERCOR_PRICE, HIPERCOR_URL, HIPERCOR_ERROR
from headers.headers import PROXIES, USER_AGENTS


class Hipercor:
  def __init__ (self):
    df1 = pd.read_json(CORTE_INGLES_DATA)
    df2 = pd.read_json(HIPERCOR_DATA)
    self.hipercorDf = pd.concat([df1, df2])

  
  def headers (self):
    # hipercor da problemas con un user-agent randomizado en el import requests

    return {
      'authority': 'www.hipercor.es',
      'cache-control': 'max-age=0',
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'sec-ch-ua-mobile': '?0',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'navigate',
      'proxy': random.choice(PROXIES).replace('\n', ''),
      'sec-fetch-user': '?1',
      'sec-fetch-dest': 'document',
      'referer': 'https://www.hipercor.es/supermercado/buscar/?term={name}&search=text',
      'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
      'cookie': 'store=hipercorStore; session_id=c6c5fc035f250fa1289ef951968f2bae73caa25baf3b7222b2eb5f61c581da3a; centre=NULL; cookiesPolicy=10001; locale=es; bm_sz=6D2718A174224DC79A818C7DD5C84A9F~YAAQvtMRAkl8UEp7AQAAJ2ZAagxGOxQ+eTIVKP4nLwJaLYr6v+klkaL9+Y4k41qtSNVDjdNB2A5GZfTWUeCa+7p/WFmDNIJ5ajXeuRvQLbJx9CcndvLLCiaMbvmE1TVkh+nvvRcFHjOOK9HUQhVMjCuy5WQRnn+kPruNWLdP3RfH/aFDsF9uUDEEqefKE8JinV8pNx/9nVW+8V23Kk+/6dsjO7kfO4XKHNmQMZ5rdDBfaMXLpMiBOpWNl1to603220nz1pxHCpgdRcnEaNGDz4j7VGjCeykDGeVZ2gtQeKQ/KN7g~3752499~4274500; bm_mi=18E5271B9C2BAF0FFFF07E36CE4B51B8~Zw8sSgJhzY3cMmTGQM4fhLgVcvi7mnsm+hYfUgfRK7bVPoQK2cS5Ur/jSMY/Irmor7Xt23Kwp9GUTJxABV3bUV7JsesHNlZm1vD9sDm24JSJ2EAvCIroLIu/6EU86YhBrKyNUzXhSJGvMsWgaojxlcd1Ns41OWjMgtCs96bSJiMFSpgDKqjhHR6oRSdxircF0h4CdZ1EqqjI4mfuNP+RUlv20FmCY3gCoNLqpQwacOhcCb/tM4iuxe8wQRKnb41+; _abck=15DDA598166564D6C926733DD5BB0899~0~YAAQvtMRAoZ8UEp7AQAAS3lAagbEy+wH+DhUI99+2BT2nFHgF44PZNApM65AMw6bZFlXAejh1HNgQdQpAxpfkGF142U0lTAGxvE5N8y+QxJ//zTCDPIWRJ7TFLiz6YuJkn+AM72xUm/Wc8B7zF91LT5rmr0iw84xJuhbVCIfOHccnbUK2WIaHJEV6If50TR7z+nNH9sJm2IdG6LAtCzms3oYJw1/+i37BGohXdSgrOO6bkW9e2xKAxq3blP1eicAVs6HsqL7UvQ+F0X5IHhlddOpvkEYmrtRDpdrSzul1w/r4k5Kja2umwkasYvnOl4xVl4u35Im7kel9joSBVwPLxj3iygw0BXeOCeAvflV6vNQOsCGE9PZVglI+6LRI7Wwd9W0OFHveZTm9CDr+gwmVfKJnvHSCs6B~-1~-1~-1; ak_bmsc=5E27D1C721B570ED2D1DD78146342676~000000000000000000000000000000~YAAQvtMRAod8UEp7AQAAS3lAagzLg8NQkvm/1jmOhdju4kobTVOKd8zwW6ir/gm9faKwHVWQmAtU/gcsrNMWeGzeKkNPEKtxwhpLQkDEfwJsXe+Z4MVVPXYofMe62uxLrbqyuFbXYORzPkCYHN/QzgospvfN9OPGAAV9735aCo7EP0qmdUkX8P3WCQVaWWdpADHx/YkDQyi2PM/an7OGSECDhvawmEHkhzkSdO2lgApUtYo6PhiGrHttso/gD8GGRSh+uGTrulHGlrwvQ3yfMN+JBJkcLKc7G+xQlO5YjrcH/tas1EX01pyr3I2yb0FifZWiIy2A9Wwu91vNDkCijl2LkeMLYFbe2+9em2pA4Jt3jVSL4MJmKiqitSDNnHwnYMcTQLuv7DgfSUFT25Yv77Rph/gt3yZv3G6312bX4YrQ/oaeSmsDNt3hVkiIvzq2KZln9wx64eW4tJnmBNxt; ADRUM_BT=R:71|i:1747410|g:e345369d-6587-4f11-9310-6a039693742b1710|e:218|n:ElCorteIngles_21ebfd29-5ff5-438e-8f46-bd65ec7500ec',
    }

  def params (product):
    return (
      ('term', product),
      ('search', 'text')
    )

  def priceList (self, productSoup):

    priceContainer = productSoup.find_all('div', class_='prices-price _current')
    return [ float(e.text.replace('\n', '').replace(' ', '').replace('€', '').replace(',', '.')) for e in priceContainer ]


  def getAverage (self, priceList):
    return sum(priceList) / len(priceList)

  def initializeScraper (self):
    priceDf = pd.DataFrame()
    errorDf = pd.DataFrame()
    for index, row in tqdm(self.hipercorDf.iterrows(), total=self.hipercorDf.shape[0]):
      
      name = row['product_name_es'] if row['product_name_es'] else row['product_name']

      try: 
        page = requests.get(HIPERCOR_URL, headers=self.headers(), params=self.params(name))
        priceList = self.priceList(BeautifulSoup(page.content, 'html.parser'))

        if priceList:
          priceDf = priceDf.append({'id': str(row['_id']),'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': self.getAverage(priceList)}, ignore_index=True, verify_integrity=False)
        else:
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name': row['product_name'], 'product_name_es': row['product_name_es'], 'price': 0.00}, ignore_index=True, verify_integrity=False)
      except ValueError:
        print("Response content is not valid Json")
        errorDf = errorDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': float(0.00)}, ignore_index=True, verify_integrity=False)
        pass

    priceDf.to_csv(HIPERCOR_PRICE, index=False)
    errorDf.to_csv(HIPERCOR_ERROR, index=False)