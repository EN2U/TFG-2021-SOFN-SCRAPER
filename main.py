from constants import constants

from scrapers.Alcampo import Alcampo
from scrapers.Carrefour import Carrefour

def evaluateName (name):
  if name == constants.ALCAMPO:
    alcampoScraper = Alcampo()
    alcampoScraper.initializeScraper()
  if name == constants.CARREFOUR:
    carrefourScraper = Carrefour()
    carrefourScraper.initializeScraper()

if __name__ == "__main__":
  ### Id del supermercado
  name = "carrefour"
  evaluateName(name)
