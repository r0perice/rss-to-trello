import requests
import json

from base_utils import BaseUtils

class CardUtils:

    rss_feed_board_id = ""
    key = ""
    token = ""

    def __init__(self, rss_feed_board_id, key, token):
        super().__init__()
        self.rss_feed_board_id = rss_feed_board_id
        self.key = key
        self.token = token

    def create_card_in_list(self, list_id, card_name):
        url = "https://api.trello.com/1/cards"

        query = self.get_base_query()
        query['idList'] = list_id
        query['name'] = card_name


        response = requests.request(
            "POST",
            url,
            params=query
        )
    
    def get_cards_id_in_list(self, list_id):
        url = "https://api.trello.com/1/lists/" + list_id + "/cards"

        query = self.get_base_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        cards_id_list = []
        list_of_dictionaries = json.loads(response.text)
        for dictionary in list_of_dictionaries:
            for k,v in dictionary.items():
                if k == "id":
                    cards_id_list.append(v)
        return cards_id_list

    def get_cards_names_in_list(self, list_id):
        url = "https://api.trello.com/1/lists/" + list_id + "/cards"

        query = self.get_base_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        cards_id_list = []
        list_of_dictionaries = json.loads(response.text)
        for dictionary in list_of_dictionaries:
            for k,v in dictionary.items():
                if k == "name":
                    cards_id_list.append(v)
        return cards_id_list


    def get_card_name_from_id(self, card_id):
        url = "https://api.trello.com/1/cards/" + card_id 

        query = self.get_base_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        dic = json.loads(response.text)
        return dic['name']


    def get_card_attachment_json(self, card_id):
        url = "https://api.trello.com/1/cards/"+ card_id + "/attachments"

        query = self.get_base_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        dic = json.loads(response.text)
        if dic:
            return dic[0]
        else:
            return None

    def get_attachment_url_from_json(self, attachment_json):
        return attachment_json['url']


    def get_base_query(self):
        query = {
            'key': self.key,
            'token': self.token
        }
        return query


    def get_rss_feed_board_id(self):
        return self.rss_feed_board_id