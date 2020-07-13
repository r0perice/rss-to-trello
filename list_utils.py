import requests
import json

from card_utils import CardUtils
from base_utils import BaseUtils
from config_keys import ApiAccess, Trello
from trello_api_constants import Lists, Boards

class ListUtils(BaseUtils):

    def __init__(self, config):
        super().__init__(config)
        self.card_utils = CardUtils(config)


    def get_list_id_from_name(self, list_name):
        rss_feed_board_id = super().get_rss_feed_board_id()
        url = Boards.MAIN_API_PREFIX + rss_feed_board_id + Lists.LISTS_SUFFIX

        query = super().build_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        dic = json.loads(response.text)
        for list_item in dic:
            for k,v in list_item.items():
                if k == "name" and v == list_name:
                    return list_item['id']


    def create_feeds_lists(self):
        feeds_list_id = self.get_list_id_from_name("Feeds")
        cards_id_list = self.card_utils.get_cards_id_in_list(feeds_list_id)
        all_list_names = self.get_all_list_names()

        for card_id in cards_id_list:
            list_name = self.card_utils.get_card_name_from_id(card_id)

            if not list_name in all_list_names:
                self.create_list(list_name)


    def clean_feed_list(self):
        feeds_list_id = self.get_list_id_from_name("Feeds")
        feeds_card_names = self.card_utils.get_cards_names_in_list(feeds_list_id)

        all_list_names = self.get_all_list_names()
        for list_name in all_list_names:

            if not list_name in feeds_card_names and list_name != "Feeds" :
                list_id = self.get_list_id_from_name(list_name)
                self.delete_list_from_id(list_id)    

 
    def delete_list_from_id(self, list_id):
        url = Lists.MAIN_API_PREFIX + list_id + Lists.LISTS_CLOSED_SUFFIX

        pre_query = {'value':'true'}
        query = super().build_query(pre_query)

        response = requests.request(
            "PUT",
            url,
            params=query
        )

    def create_list(self, list_name):
        feeds_list_id = self.get_list_id_from_name("Feeds")
        feeds_list_pos = self.get_list_pos_from_id(feeds_list_id)
        new_list_pos = feeds_list_pos + 1

        url = Lists.MAIN_API_PREFIX

        
        pre_query = {
                    'name':list_name,
                    'idBoard':super().get_rss_feed_board_id(),
                    'pos':new_list_pos
                    }
        query = super().build_query(pre_query)
        

        requests.request(
            "POST",
            url,
            params=query
        )


    def get_list_pos_from_id(self, list_id):
        url = Lists.MAIN_API_PREFIX + list_id

        query = super().build_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        dic = json.loads(response.text)
        return dic['pos']


    def get_all_list_ids(self):
        rss_feed_board_id = super().get_rss_feed_board_id()
        url = Boards.MAIN_API_PREFIX + rss_feed_board_id + Lists.LISTS_SUFFIX

        query = super().build_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        ids = []
        dic = json.loads(response.text)
        for list_item in dic:
            for k,v in list_item.items():
                if k == "id":
                    ids.append(v)
        return ids

    def get_all_list_names(self):
        rss_feed_board_id = super().get_rss_feed_board_id()
        url = Boards.MAIN_API_PREFIX + rss_feed_board_id + Lists.LISTS_SUFFIX

        query = super().build_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        ids = []
        dic = json.loads(response.text)
        for list_item in dic:
            for k,v in list_item.items():
                if k == "name":
                    ids.append(v)
        return ids

    def get_card_utils(self):
        return self.card_utils