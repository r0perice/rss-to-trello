import requests
from requests import Response
import json

from card_utils import CardUtils
from base_utils import BaseUtils
from config_keys import ApiAccess, Trello
from trello_api_constants import Lists, Boards, Cards

class ListUtils(BaseUtils):

    FEEDS_BOARD_NAME = "Feeds"

    def __init__(self, config: dict):
        super().__init__(config)
        self.card_utils = CardUtils(config)


    def get_list_id_from_name(self, list_name: str) -> dict:
        rss_feed_board_id: str = super().get_rss_feed_board_id()
        url: str = Boards.MAIN_API_PREFIX + rss_feed_board_id + Lists.LISTS_SUFFIX

        query: dict = super().build_query()

        response: Reponse = requests.get(url, query)

        dict_response = super().convert_response_into_dict(response)
        for list_item in dict_response:
            for key,value in list_item.items():
                if key == "name" and value == list_name:
                    return list_item['id']


    def create_feeds_lists(self):
        feeds_list_id = self.get_list_id_from_name(self.FEEDS_BOARD_NAME)
        cards_id_list = self.card_utils.get_cards_id_in_list(feeds_list_id)
        all_list_names = self.get_all_list_names()

        for card_id in cards_id_list:
            list_name = self.card_utils.get_card_name_from_id(card_id)
            attachement = self.card_utils.get_card_attachment_json(card_id)
            if (not list_name in all_list_names) and (attachement is not None) :
                self.create_list(list_name)


    def clean_feed_list(self) -> None:
        feeds_list_id = self.get_list_id_from_name(self.FEEDS_BOARD_NAME)
        feeds_card_names = self.card_utils.get_cards_names_in_list(feeds_list_id)
        all_list_names = self.get_all_list_names()

        for list_name in all_list_names:
            if not list_name in feeds_card_names and list_name != self.FEEDS_BOARD_NAME :
                list_id = self.get_list_id_from_name(list_name)
                self.delete_list_from_id(list_id)    

 
    def delete_list_from_id(self, list_id: str) -> None:
        url = Lists.MAIN_API_PREFIX + list_id + Lists.LISTS_CLOSED_SUFFIX

        pre_query = {'value':'true'}
        query = super().build_query(pre_query)

        requests.put(url, query)


    def create_list(self, list_name: str) -> None:
        feeds_list_id = self.get_list_id_from_name(self.FEEDS_BOARD_NAME)
        feeds_list_pos = self.get_list_pos_from_id(feeds_list_id)
        new_list_pos = feeds_list_pos + 1

        url = Lists.MAIN_API_PREFIX

        pre_query = {
                    'name':list_name,
                    'idBoard':super().get_rss_feed_board_id(),
                    'pos':new_list_pos
                    }
        query = super().build_query(pre_query)

        requests.post(url, query)


    def get_list_pos_from_id(self, list_id: str) -> str:
        url = Lists.MAIN_API_PREFIX + list_id

        query = super().build_query()

        response = requests.get(url, query)
        dict_response = super().convert_response_into_dict(response)

        return dict_response.get('pos')


    def get_all_list_ids(self) -> dict:
        rss_feed_board_id: str = super().get_rss_feed_board_id()
        url = Boards.MAIN_API_PREFIX + rss_feed_board_id + Lists.LISTS_SUFFIX

        query = super().build_query()

        response = requests.get(url, query)
        dict_response = super().convert_response_into_dict(response)

        ids = []
        for list_item in dict_response:
            for key in list_item.keys():
                if key == "id":
                    ids.append(v)
        return ids


    def get_all_list_names(self) -> dict:
        rss_feed_board_id = super().get_rss_feed_board_id()
        url = Boards.MAIN_API_PREFIX + rss_feed_board_id + Lists.LISTS_SUFFIX

        query = super().build_query()

        response = requests.get(url, query)

        dict_response = json.loads(response.text)

        ids = []
        for list_item in dict_response:
            for key,value in list_item.items():
                if key == "name":
                    ids.append(value)
        return ids


    def get_number_of_cards_in_list(self, list_id: str) -> int:
        url = Lists.MAIN_API_PREFIX + list_id + Cards.CARDS_SUFFIX

        query = super().build_query()

        response = requests.get(url, query)

        dict_response = super().convert_reponse_into_list_dict(response)
        return len(dict_response)


    def get_card_utils(self) -> CardUtils:
        return self.card_utils