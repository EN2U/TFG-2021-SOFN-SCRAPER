from constants import constants

from scrapers.Alcampo import Alcampo
import pandas as pd

def evaluateName (name):
  if name == constants.ALCAMPO:
    alcampoScraper = Alcampo(pd.read_json("./dataScraped/alcampo/parsedAlcampo.json"))
    alcampoScraper.initializeScraper()
  if name == constants.CARREFOUR:
    print()

if __name__ == "__main__":
  ### Id del supermercado
  name = "alcampo"
  evaluateName(name)
