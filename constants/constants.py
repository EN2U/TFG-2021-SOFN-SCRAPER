import codecs
import os

# Custom id of stores
ALCAMPO_ID = "0"
CARREFOUR_ID = "1"
HIPERCOR_ID = "2"
DIA_ID = "3"
MERCADONA_ID = "4"
EROSKI_ID = "5"

# Petition store url 
ALCAMPO_URL = 'https://www.alcampo.es/compra-online/search/'
CARREFOUR_URL = 'https://www.carrefour.es/search-api/query/v1/search'
EROSKI_URL = 'https://supermercado.eroski.es/es/search/results/'
""" HIPERCOR_URL
HIPERCOR_URL
MERCADONA_URL """

# Data json store location 

ALCAMPO_DATA = './dataScraped/alcampo/parsedAlcampo.json'
AUCHAN_DATA = './dataScraped/alcampo/parsedAuchan.json'

CARREFOUR_DATA = './dataScraped/carrefour/parsedCarrefour.json' 

CORTE_INGLES_DATA = './dataScraped/hipercor/parsedCorteIngles.json'
HIPERCOR_DATA = './dataScraped/hipercor/parsedHipercor.json'

MERCADONA_DATA = './dataScraped/mercadona/parsedMercadona.json'

EROSKI_DATA = './dataScraped/eroski/parsedEroski.json'

DIA_DATA = './dataScraped/dia/parsedDia.json'

# Output route of prices data

ALCAMPO_PRICE = './dataScraped/alcampo/alcampoPrices.csv'
ALCAMPO_ERROR = './dataScraped/alcampo/alcampoError.csv'


CARREFOUR_PRICE = './dataScraped/carrefour/carrefourPrices.csv' 
CARREFOUR_ERROR = './dataScraped/carrefour/carrefourError.csv'

HIPERCOR_PRICE = './dataScraped/hipercor/hipercorPrices.csv'
HIPERCOR_ERROR = './dataScraped/hipercor/hipercorError.csv'

MERCADONA_PRICE = './dataScraped/mercadona/mercadonaPrices.csv'
MERCADONA_ERROR = './dataScraped/mercadona/mercadonaError.csv'

EROSKI_PRICE = './dataScraped/eroski/eroskiPrices.csv'
EROSKI_ERROR = './dataScraped/eroski/eroskiError.csv'

DIA_PRICE = './dataScraped/dia/diaPrices.csv'
DIA_ERROR = './dataScraped/dia/diaError.csv'