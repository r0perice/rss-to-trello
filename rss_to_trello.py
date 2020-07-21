import requests
import feedparser
import json
import schedule
import time
import hashlib

from tinydb import TinyDB, Query
from card_utils import CardUtils
from list_utils import ListUtils
from board_utils import BoardUtils
from rss_parser_utils import RssParserUtils
from database_utils import DatabaseUtils
from config_keys import ApiAccess, Trello



class RssToTrello:

    def __init__(self, rss_parser_utils: RssParserUtils):
        self.rss_parser_utils = rss_parser_utils
        self.list_utils = rss_parser_utils.list_utils

    def create_labels(self) -> None:
        self.rss_parser_utils.board_utils.create_label_on_board(BoardUtils.MISSING_RSS_FEED_URL_LABEL_NAME, "red")
        self.rss_parser_utils.board_utils.create_label_on_board(BoardUtils.MISSING_RSS_FEED_URL_LABEL_NAME, "green")
        self.rss_parser_utils.board_utils.create_label_on_board(BoardUtils.NEW_ARTICLES_LABEL_NAME, "purple")
        self.rss_parser_utils.board_utils.create_label_on_board(BoardUtils.OLD_ARTICLES_LABEL_NAME, "black")

    def refresh_lists(self) -> None:
        self.list_utils.refresh_board()
        self.rss_parser_utils.register_rss_feeds()
    
    def refresh_rss(self) -> None:
        self.rss_parser_utils.refresh_rss_feed()



db = TinyDB('C:/Users/Robin Perice/Desktop/rss-to-trello.json')

config = { 
        ApiAccess.TRELLO_API_KEY:slack_api_key,
        ApiAccess.TRELLO_API_TOKEN:slack_api_token,
        Trello.RSS_FEED_BOARD_ID:rss_feed_board_id
        }

database_util = DatabaseUtils(db)
list_util = ListUtils(config)
board_utils = BoardUtils(config)
parser = RssParserUtils(database_util, list_util, board_utils)
rss = RssToTrello(parser)
rss.create_labels()


## MAIN LOOP
schedule.every(1).seconds.do(rss.refresh_lists)
schedule.every(10).seconds.do(rss.refresh_rss)


while True:
    schedule.run_pending()
    time.sleep(1)