import feedparser

from card_utils import CardUtils
from list_utils import ListUtils
from board_utils import BoardUtils
from database_utils import DatabaseUtils
from card import Card

class RssParserUtils:

    card_name_and_rss_feeds = {}

    def __init__(self, database_utils: DatabaseUtils, list_utils: ListUtils, board_utils: BoardUtils):
        self.database_utils = database_utils
        self.card_utils = list_utils.get_card_utils()
        self.list_utils = list_utils
        self.board_utils = board_utils

    def register_rss_feeds(self) -> None:
       # try:
            feeds_list_id = self.list_utils.get_list_id_from_name("Feeds")
            feeds_card_ids = self.card_utils.get_cards_id_in_list(feeds_list_id)

            for feeds_card_id in feeds_card_ids:
                
                card_attachment_json = self.card_utils.get_card_attachment_json(feeds_card_id)
                if card_attachment_json is None:
                    self.board_utils.set_card_label(feeds_card_id, "Missing Rss Feed Url")
                else:
                    self.board_utils.set_card_label(feeds_card_id, "Rss Feed Ok")
                    card_attachment_url = self.card_utils.get_attachment_url_from_json(card_attachment_json)
                    if card_attachment_url is not None:
                        card_name = self.card_utils.get_card_name_from_id(feeds_card_id)
                        self.card_name_and_rss_feeds[card_name] = card_attachment_url
        #except Exception as e:
         #   print(str(e))


    def refresh_rss_feed(self) -> None:
        try:
            for card_name,rss_feed_url in self.card_name_and_rss_feeds.items():
                last_articles = feedparser.parse(rss_feed_url)
                list_id = self.list_utils.get_list_id_from_name(card_name)

                nb = self.list_utils.get_number_of_cards_in_list(list_id)

                for article in last_articles.entries:
                    if nb < 6:
                        article_url = article.link
                        if not self.database_utils.if_article_in_database(article_url):
                            card_pos = self.card_utils.get_card_pos_in_list(self.list_utils.headers_name_and_id.get(BoardUtils.NEW_ARTICLES_LABEL_NAME + list_id))
                            card = Card(article)
                            card_id = self.card_utils.create_card_in_list(list_id, card, str(card_pos))
                            self.database_utils.put_article_in_database(article_url)
                            nb = nb + 1
        except Exception as e:
            print(str(e))