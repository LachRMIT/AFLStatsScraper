from src.models import *
from db.db_manager import AFLDBTools
from src.scraper.AFLTablesScraper import AFLTablesScraper
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/afl_scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

dbm = AFLDBTools()
scraper = AFLTablesScraper()

dbm.drop_tables()

