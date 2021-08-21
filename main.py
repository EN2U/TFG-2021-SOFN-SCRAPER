from constants import constants

from scrapers.Alcampo import Alcampo
from scrapers.Carrefour import Carrefour
from scrapers.Hipercor import Hipercor
from scrapers.Dia import Dia
from scrapers.Mercadona import Mercadona
from scrapers.Eroski import Eroski



def evaluateName (name):
  if name == constants.ALCAMPO_ID:
    alcampoScraper = Alcampo()
    alcampoScraper.initializeScraper()
  if name == constants.CARREFOUR_ID:
    carrefourScraper = Carrefour()
    carrefourScraper.initializeScraper()
  if name == constants.HIPERCOR_ID:
    hipercorScraper = Hipercor()
    hipercorScraper.initializeScraper()
  if name == constants.DIA_ID:
    diaScraper = Dia()
    diaScraper.initializeScraper()
  if name == constants.MERCADONA_ID:
    mercadonaScraper = Mercadona()
    mercadonaScraper.initializeScraper()
  if name == constants.EROSKI_ID:
    eroskiScraper = Eroski()
    eroskiScraper.initializeScraper()
if __name__ == "__main__":
  ### Id del supermercado
  name = input('[0] alcampo/auchan, [1] carrefour, [2] hipercor/corte ingles, [3] dia, [4] mercadona, [5] eroski')
  print(name)
  evaluateName(name)
