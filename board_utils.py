import requests

from base_utils import BaseUtils
from trello_api_constants import Cards, Labels


class BoardUtils(BaseUtils):

    MISSING_RSS_FEED_URL_LABEL_NAME = "Missing RSS feed url"
    RSS_FEED_OK_LABEL_NAME = "RSS feed OK"
    NEW_ARTICLES_LABEL_NAME = "New articles"
    OLD_ARTICLES_LABEL_NAME = "Old articles"

    # 'key: label_name, value: color_name'
    labels_and_ids = {}

    def __init__(self, config: dict):
        super().__init__(config)

    def create_label_on_board(self, label_name: str, label_color: str) -> None:
        """
        Create a label with a name and a color.
        Available colors are yellow, purple, blue, red, 
        green, orange, black, sky, pink, lim
        """
        url = Labels.MAIN_API_PREFIX

        pre_query = {
                    'name':label_name,
                    'color':label_color,
                    'idBoard': super().get_rss_feed_board_id()
                    }
        query = super().build_query(pre_query)

        response = requests.post(url, query)
        dict_response = super().convert_response_into_dict(response)
        print(response.content)
        self.labels_and_ids[label_name] = dict_response.get('id')


    def set_card_label(self, card_id: str, label_name: str) -> None:
        url = Cards.MAIN_API_PREFIX + card_id + "/idLabels"

        pre_query = {
                    'id': card_id,
                    'value': self.labels_and_ids.get(label_name)
                    }
        query = super().build_query(pre_query)

        response = requests.post(url, query)
