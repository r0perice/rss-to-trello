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



card_name_and_rss_feeds = {}


class RssToTrello:

    rss_parser_utils = None
    list_utils = None

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

database_util = DatabaseUtils(db)
card_utils = CardUtils(rss_feed_board_id,slack_api_key,slack_api_token)
list_util = ListUtils(card_utils,rss_feed_board_id,slack_api_key,slack_api_token)
parser = RssParserUtils(database_util, card_utils, list_util)
rss = RssToTrello(parser,)


## MAIN LOOP
schedule.every(1).seconds.do(rss.refresh_list)
schedule.every(10).seconds.do(rss.refresh_rss)


while True:
    schedule.run_pending()
    time.sleep(1)