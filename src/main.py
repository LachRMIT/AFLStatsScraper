from src.models import *
# from db.db_manager import AFLDBTools
from src.scraper.AFLTablesScraper import AFLTablesScraper

scraper = AFLTablesScraper()
scraper.set_year(2024)

season = scraper.scrape_season()
