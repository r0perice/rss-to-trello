import requests
import json

from card_utils import CardUtils

class ListUtils:

    rss_feed_board_id = ""
    key = ""
    token = ""
    card_utils = None
    def __init__(self, card_utils, rss_feed_board_id, key, token):
        super().__init__()
        self.rss_feed_board_id = rss_feed_board_id
        self.key = key
        self.token = token
        self.card_utils = card_utils


    def get_list_id_from_name(self, list_name):
        rss_feed_board_id = self.get_rss_feed_board_id()
        url = "https://api.trello.com/1/boards/" + rss_feed_board_id + "/lists"

        query = self.get_base_query()

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
        url = "https://api.trello.com/1/lists/" + list_id +"/closed"

        query = self.get_base_query()
        query['value'] = 'true'

        response = requests.request(
            "PUT",
            url,
            params=query
        )

    def create_list(self, list_name):
        feeds_list_id = self.get_list_id_from_name("Feeds")
        feeds_list_pos = self.get_list_pos_from_id(feeds_list_id)
        new_list_pos = feeds_list_pos + 1

        url = "https://api.trello.com/1/lists"

        query = self.get_base_query()
        query['name'] = list_name
        query['idBoard'] = self.get_rss_feed_board_id()
        query['pos'] = new_list_pos
        

        requests.request(
            "POST",
            url,
            params=query
        )


    def get_list_pos_from_id(self, list_id):
        url = "https://api.trello.com/1/lists/" + list_id

        query = self.get_base_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        dic = json.loads(response.text)
        return dic['pos']


    def get_all_list_ids(self):
        rss_feed_board_id = self.get_rss_feed_board_id()
        url = "https://api.trello.com/1/boards/" + rss_feed_board_id + "/lists"

        query = self.get_base_query()

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
        rss_feed_board_id = self.get_rss_feed_board_id()
        url = "https://api.trello.com/1/boards/" + rss_feed_board_id + "/lists"

        query = self.get_base_query()

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


    def get_base_query(self):
        query = {
             'key': self.key,
            'token': self.token
        }
        return query


    def get_rss_feed_board_id(self):
        return self.rss_feed_board_id