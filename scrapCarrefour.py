import requests
import pandas as pd
import random
import json

from tqdm import tqdm
from bs4 import BeautifulSoup
from headers.headers import PROXIES, USER_AGENTS


def initializeHeader ():
  user_agent = random.choice(USER_AGENTS)
  proxy = random.choice(PROXIES)
  proxy = proxy.replace('\n', '')
  print (proxy)
  return {
        'authority': 'www.carrefour.es',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'accept': '*/*',
        'User-agent': user_agent,
        'http': proxy,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.carrefour.es/search?q=chocolate',
        'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
        'cookie': 'visid_incap_258278=30DWicCMSpuM8SjAJvTwVli7x2AAAAAAQUIPAAAAAADmOFXUsLQiz7kSXP8tUPmX; visid_incap_769673=Kej6pG2cRMO6t4a0G3Ew9Fi7x2AAAAAAQUIPAAAAAADQT+4sllJniJFQtSl/m0sE; cookiergpdinfo=false-3; cookiergpd=true-true-true-true; nlbi_258278_1838428=beKnONW4Wnt/IK2gkFHSqAAAAACeseLqmHCKCbFBOW3+6neK; nlbi_258278=UHodDArv02AR+ygXkFHSqAAAAAAgvIDEUxjqz6dZe+Rp0NKt; incap_ses_1297_769673=H4iMDg5bDgpIo2my5t7/EYagHmEAAAAAGm9gerPNcGnMPftQfxbSUA==; incap_ses_1297_258278=rDb+YkJ34VKe0nmy5t7/ETqoHmEAAAAAlwRcTln2ACaA7+J3J+Jrsw==; session_id=1wzIU50gKC6eBW5rX1GleAgubzG; incap_ses_1396_258278=ViBKRppoS3NHcHXJzZZfE5qCH2EAAAAArpdMpYXdG5M45hRJFnG6/A==; incap_ses_1396_769673=w9HiKQQ/xEA7uX3JzZZfE9qFH2EAAAAANRBLT/zS7oDTGxCQhtYhhQ==; JSESSIONID=zTZ8Q2VIkkUUoCXl1sh2tMyX.sf2_7; ATG_SESSION_ID=zTZ8Q2VIkkUUoCXl1sh2tMyX.sf2_7; userPrefLanguage=es_ES; PROFILE_ID=6591690197; collage_state="zeICrqkGeuMuyq/17QzDClJ+Kjc597oe/9gqxaqsvDvKyTFmjprqk1WEQvvfs6Hl04598u2yD+vfl1MyovyxMpMZvnnWZGhY7B39m29rLom3w7qDueuAlEHyCZEe0kTT0vNHtm7ZYe0wuqEzpQ2KHOkIKWUfZV2E83ioge7kZEPioHTjEi2JPajazvuxzGo5nuJICxesPUo4jYUwC0Ap/lpyZ07egbPlJ/EXs78Q65buDKmYMgf/ehczugh/2D3l9GF+GoBu8thXgI28KZ7roFDkaL7NsORzC/c2/cucFs1hBkYISzvpqA4PfVU3ZLJ3PTB4a3RSFBJenEKKkU2UiBNUI6654oFlGkaMvvT89v7Kniwa1ZBHnBe7kh7Uxg2zYCV0ufjE0jNu8NeBatDAVu/Rhs4KOxBWQ9DUHA+krt5r0llGa7n492syW3ali1A4ecdoIlk+sH1AvDRWDl5V/ysfVUo2yPV1Ul1WAl7VRJL41NjCIYtiz+gRLhNGU5aJ2LIzvwMiuSpUD5KqE0f16RsE1tfiVF1MKr2UUwu4M7o="',
    }

def initializeParams (product):
  return (
        ('query', product),
        ('scope', 'desktop'),
        ('lang', 'es'),
        ('user', '10632999-e337-40c1-abb8-e89a291c0221'),
        ('session', '061ed29a-a36f-4da6-8c09-3be0870b5260'),
        ('user_type', 'recurrent'),
        ('rows', '24'),
        ('start', '0'),
        ('origin', 'linked'),
        ('f.op', 'OR'),
    )

def initializePriceList (productSoup):
    
    priceContainer = productSoup.find_all('strong', class_='ebx-result-price__value')
    priceContainer = priceContainer[2:len(priceContainer)]
    priceList = list()
    


    for item in priceContainer:
        priceList.append(item.text)

    
    priceList = [x.replace('\n', '').replace(' ', '') for x in priceList]
    print(priceList)
    
    return priceList


def initializeProductList (productSoup):
    
    productsContainer = productSoup.find_all('h1', class_='ebx-result-title ebx-result__title')
    print(productsContainer)
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
    avgPrice = avgPrice + price
  return avgPrice / len(priceList)

def carrefourScrap (df):
    priceDf = pd.DataFrame()

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        
        headers = initializeHeader()

        params = initializeParams(row['product_name_es'] if row['product_name_es'] else row['product_name'])
        page = requests.get('https://www.carrefour.es/search-api/query/v1/search', headers=headers, params=params)

        if page.content:
          test = json.loads(page.content)
          priceList = [ float(e['active_price']) for e in test['content']['docs'] ]
          priceDf = priceDf.append({'id': str(row['_id']), 'product_name_es': row['product_name_es'], 'product_name': row['product_name'], 'price': getAverage(priceList) if priceList else float(0.00)}, ignore_index=True, verify_integrity=False)
        else:
          print ("empty")

    priceDf.to_csv("carrefourPrices.csv", index=False)

    
if __name__ == "__main__":

    df = pd.read_json("./parsedCarrefour.json")
    print (len(df.index))
    carrefourScrap(df)