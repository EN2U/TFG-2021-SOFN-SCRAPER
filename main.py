from constants import constants

from scrapers.Alcampo import Alcampo
from scrapers.Carrefour import Carrefour
from scrapers.Hipercor import Hipercor
from scrapers.Dia import Dia
from scrapers.Mercadona import Mercadona
from scrapers.Eroski import Eroski



def evaluateName (name):
  if name == constants.ALCAMPO:
    alcampoScraper = Alcampo()
    alcampoScraper.initializeScraper()
  if name == constants.CARREFOUR:
    carrefourScraper = Carrefour()
    carrefourScraper.initializeScraper()
  if name == constants.HIPERCOR:
    hipercorScraper = Hipercor()
    hipercorScraper.initializeScraper()
  if name == constants.DIA:
    diaScraper = Dia()
    diaScraper.initializeScraper()
  if name == constants.MERCADONA:
    mercadonaScraper = Mercadona()
    mercadonaScraper.initializeScraper()
  if name == constants.EROSKI:
    eroskiScraper = Eroski()
    eroskiScraper.initializeScraper()
if __name__ == "__main__":
  ### Id del supermercado
  name = "eroski"
  evaluateName(name)
