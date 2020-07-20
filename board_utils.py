import requests

from base_utils import BaseUtils
from trello_api_constants import Cards


class BoardUtils(BaseUtils):

    MISSING_RSS_FEED_URL_LABEL_NAME = "Missing RSS feed url"
    RSS_FEED_OK_LABEL_NAME = "RSS feed OK"
    NEW_ARTICLE_LABEL_NAME = "New article"

    labels_and_ids = {}

    def __init__(self, config: dict):
        super().__init__(config)

    def create_label_on_board(self, label_name: str, label_color: str) -> None:
        url = "https://api.trello.com/1/labels/"

        ## yellow, purple, blue, red, green, orange, black, sky, pink, lime

        pre_query = {
                    'name':label_name,
                    'color':label_color,
                    'idBoard': super().get_rss_feed_board_id()
                    }
        query = super().build_query(pre_query)

        response = requests.post(url, query)
        dict_response = super().convert_response_into_dict(response)
        self.labels_and_ids[label_name] = dict_response['id']


    def set_card_label(self, card_id: str, label_name: str) -> None:
        url = Cards.MAIN_API_PREFIX + card_id + "/idLabels"

        pre_query = {
                    'id': card_id,
                    'value': self.labels_and_ids.get(label_name)
                    }
        query = super().build_query(pre_query)

        response = requests.post(url, query)
