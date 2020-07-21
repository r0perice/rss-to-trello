import requests
from requests import Response
import json

from card_utils import CardUtils
from card import Card
from base_utils import BaseUtils
from board_utils import BoardUtils
from config_keys import ApiAccess, Trello
from emoji_codes import EmojiCodes
from trello_api_constants import Lists, Boards, Cards


class ListUtils(BaseUtils):

    NEW_ARTICLES_HEADER_POSITION = 0;
    OLD_ARTICLES_HEADER_POSITION = 5;

    FEEDS_BOARD_NAME = "Feeds"

    headers_name_and_id = {}

    def __init__(self, config: dict):
        super().__init__(config)
        self.card_utils = CardUtils(config)
        self.board_utils = BoardUtils(config)


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

    def refresh_board(self):
        self.__remove_useless_lists()
        self.__create_feeds_lists()
        
        

    def __create_feeds_lists(self):
        """
        create lists in the board from the "feeds" cards' list
        """
        feeds_list_id = self.get_list_id_from_name(self.FEEDS_BOARD_NAME)
        cards_id_list = self.card_utils.get_cards_id_in_list(feeds_list_id)
        all_list_names = self.get_all_list_names()

        for card_id in cards_id_list:
            list_name = self.card_utils.get_card_name_from_id(card_id)
            attachement = self.card_utils.get_card_attachment_json(card_id)
            # if the list is not already created and if their is and attachment
            # on the "feeds" card then create the list
            if (not list_name in all_list_names) and (attachement is not None) :
                self.create_rss_list(list_name)


    def create_rss_list(self, list_name: str) -> None:
        list_id = self.create_list(list_name)

        new_articles_header_card_id = self.card_utils.create_header_card(list_id, 
            EmojiCodes.ROCKET + " " + BoardUtils.NEW_ARTICLES_LABEL_NAME, ListUtils.NEW_ARTICLES_HEADER_POSITION)
        self.headers_name_and_id[BoardUtils.NEW_ARTICLES_LABEL_NAME + list_id] = new_articles_header_card_id
        self.board_utils.set_card_label(new_articles_header_card_id, BoardUtils.NEW_ARTICLES_LABEL_NAME)

        new_articles_header_card_post = int(self.card_utils.get_card_pos_in_list(new_articles_header_card_id))
        old_articles_header_card_id = self.card_utils.create_header_card(list_id, 
            EmojiCodes.TIME + " " + BoardUtils.OLD_ARTICLES_LABEL_NAME, str(new_articles_header_card_post + 1))
        self.headers_name_and_id[BoardUtils.OLD_ARTICLES_LABEL_NAME + list_id] = old_articles_header_card_id
        self.board_utils.set_card_label(old_articles_header_card_id, BoardUtils.OLD_ARTICLES_LABEL_NAME)


    def __remove_useless_lists(self) -> None:
        """
        Remove all irrelevant lists from the board 
        """
        feeds_list_id = self.get_list_id_from_name(self.FEEDS_BOARD_NAME)
        feeds_card_names = self.card_utils.get_cards_names_in_list(feeds_list_id)
        all_list_names = self.get_all_list_names()

        for list_name in all_list_names:
            # if list is not in "feeds" cards' list and it is not "feeds" list
            if not list_name in feeds_card_names and list_name != self.FEEDS_BOARD_NAME :
                list_id = self.get_list_id_from_name(list_name)
                self.delete_list_from_id(list_id)    

 
    def delete_list_from_id(self, list_id: str) -> None:
        url = Lists.MAIN_API_PREFIX + list_id + Lists.LISTS_CLOSED_SUFFIX

        pre_query = {'value':'true'}
        query = super().build_query(pre_query)

        requests.put(url, query)


    def create_list(self, list_name: str) -> str:
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

        response = requests.post(url, query)
        dict_reponse = super().convert_response_into_dict(response)
        return dict_reponse.get('id')

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