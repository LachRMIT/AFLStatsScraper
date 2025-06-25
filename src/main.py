from src.models import *
from db.db_manager import AFLDBTools
from src.scraper.AFLTablesScraper import AFLTablesScraper
import time

dbm = AFLDBTools()
scraper = AFLTablesScraper()
scraper.set_year(2024)
season = scraper.scrape_season()

dbm.populate_round(season.get_round(1))
