from src.models import *
from db.db_manager import AFLDBTools
from src.scraper.AFLTablesScraper import AFLTablesScraper

dbm = AFLDBTools()
scraper = AFLTablesScraper()

dbm.verify_tables()
dbm.populate_db()

