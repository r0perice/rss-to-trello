import requests
import json

from base_utils import BaseUtils
from config_keys import ApiAccess, Trello
from trello_api_constants import Lists, Cards

class CardUtils(BaseUtils):


    def __init__(self, config):
       super().__init__(config)

    def create_card_in_list(self, list_id, card_name):
        url = Cards.MAIN_API_PREFIX

        pre_query = {
                    'idList':list_id,
                    'name':card_name
                    }
        query = super().build_query(pre_query)


        response = requests.request(
            "POST",
            url,
            params=query
        )
    
    def get_cards_id_in_list(self, list_id):
        url = Lists.MAIN_API_PREFIX + list_id + Cards.CARDS_SUFFIX

        query = super().build_query()

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
        url = Lists.MAIN_API_PREFIX + list_id + Cards.CARDS_SUFFIX

        query = super().build_query()

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
        url = Cards.MAIN_API_PREFIX + card_id 

        query = super().build_query()

        response = requests.request(
            "GET",
            url,
            params=query
        )

        dic = json.loads(response.text)
        return dic['name']


    def get_card_attachment_json(self, card_id):
        url = Cards.MAIN_API_PREFIX + card_id + Cards.CARDS_ATTACHMENT_SUFFIX

        query = super().build_query()

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
