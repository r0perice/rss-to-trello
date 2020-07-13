import requests
import feedparser
import json
import schedule
import time
import hashlib
from tinydb import TinyDB, Query

from card_utils import CardUtils
from list_utils import ListUtils
from rss_parser_utils import RssParserUtils
from database_utils import DatabaseUtils
from  config_keys import ApiAccess, Trello


card_name_and_rss_feeds = {}


class RssToTrello:

    def __init__(self, rss_parser_utils):
        self.rss_parser_utils = rss_parser_utils
        self.list_utils = rss_parser_utils.list_utils
    
    def refresh_list(self):
        self.list_utils.clean_feed_list()
        self.list_utils.create_feeds_lists()
        self.rss_parser_utils.registerRssFeeds()
    
    def refresh_rss(self):
        self.rss_parser_utils.refresh_rss_feed()



db = TinyDB('C:/Users/Robin Perice/Desktop/rss-to-trello.json')

config = { 
        ApiAccess.TRELLO_API_KEY:slack_api_key,
        ApiAccess.TRELLO_API_TOKEN:slack_api_token,
        Trello.RSS_FEED_BOARD_ID:rss_feed_board_id
        }

database_util = DatabaseUtils(db)
list_util = ListUtils(config)
parser = RssParserUtils(database_util, list_util)
rss = RssToTrello(parser,)


## MAIN LOOP
schedule.every(1).seconds.do(rss.refresh_list)
schedule.every(10).seconds.do(rss.refresh_rss)


while True:
    schedule.run_pending()
    time.sleep(1)