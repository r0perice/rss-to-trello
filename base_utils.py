from config_keys import ApiAccess, Trello
from trello_api_constants import Lists, Boards

class BaseUtils:

    rss_feed_board_id = ""
    key = ""
    token = ""

    def __init__(self, config):
        self.key = config.get(ApiAccess.TRELLO_API_KEY)
        self.token = config.get(ApiAccess.TRELLO_API_TOKEN)
        self.rss_feed_board_id = config.get(Trello.RSS_FEED_BOARD_ID)

    def __get_base_query(self):
        query = {
            'key': self.key,
            'token': self.token
        }
        return query

    def get_rss_feed_board_id(self):
        return self.rss_feed_board_id

    def build_query(self, *query):
        if not query:
            return self.__get_base_query()
        else:
            base_query = self.__get_base_query()
            return {**base_query, **query[0]}

