import feedparser

from card_utils import CardUtils
from list_utils import ListUtils
from database_utils import DatabaseUtils
from card import Card

class RssParserUtils:

    card_name_and_rss_feeds = {}

    def __init__(self, database_utils: DatabaseUtils, list_utils: ListUtils):
        self.database_utils = database_utils
        self.card_utils = list_utils.get_card_utils()
        self.list_utils = list_utils

    def register_rss_feeds(self) -> None:
        feeds_list_id = self.list_utils.get_list_id_from_name("Feeds")
        feeds_card_ids = self.card_utils.get_cards_id_in_list(feeds_list_id)

        for feeds_card_id in feeds_card_ids:
            
            card_attachment_json = self.card_utils.get_card_attachment_json(feeds_card_id)
            if card_attachment_json is not None:
                card_attachment_url = self.card_utils.get_attachment_url_from_json(card_attachment_json)
                if card_attachment_url is not None:
                    card_name= self.card_utils.get_card_name_from_id(feeds_card_id)
                    self.card_name_and_rss_feeds.update(card_name, card_attachment_url)


    def refresh_rss_feed(self) -> None:
        for k,v in self.card_name_and_rss_feeds.items():
            last_articles = feedparser.parse(v)
            last_articles_entries = last_articles.entries
            list_id = self.list_utils.get_list_id_from_name(k)

            for article in last_articles_entries:
                article_url = article.link
                if not self.database_utils.if_article_in_database(article_url):
                    card = Card(article)
                    self.card_utils.create_card_in_list(list_id, card)
                    self.database_utils.put_article_in_database(article_url)