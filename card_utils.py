import requests
import json

from base_utils import BaseUtils
from config_keys import ApiAccess, Trello
from trello_api_constants import Lists, Cards
from card import Card

class CardUtils(BaseUtils):


    def __init__(self, config: dict):
       super().__init__(config)

    def create_card_in_list(self, list_id: str, card: Card) -> None:
        url = Cards.MAIN_API_PREFIX

        pre_query = {
                    'idList':list_id,
                    'name':card.get_title(),
                    'desc':self.build_description(card),
                    'urlSource ':card.get_link()
                    }
        query = super().build_query(pre_query)

        requests.post(url, query)

    
    def get_cards_id_in_list(self, list_id: str) -> dict:
        url = Lists.MAIN_API_PREFIX + list_id + Cards.CARDS_SUFFIX

        query = super().build_query()

        response: Response = requests.get(url, query)
        list_of_dictionaries = super().convert_reponse_into_list_dict(response)

        cards_id_list = []
        for dictionary in list_of_dictionaries:
            for key,value in dictionary.items():
                if key == "id":
                    cards_id_list.append(value)
        return cards_id_list


    def get_cards_names_in_list(self, list_id: str) -> dict:
        url = Lists.MAIN_API_PREFIX + list_id + Cards.CARDS_SUFFIX

        query = super().build_query()

        response = requests.get(url, query)
        list_of_dictionaries = super().convert_response_into_dict(response)

        cards_id_list = []
        for dictionary in list_of_dictionaries:
            for k,v in dictionary.items():
                if k == "name":
                    cards_id_list.append(v)
        return cards_id_list


    def get_card_name_from_id(self, card_id: str) -> str:
        url = Cards.MAIN_API_PREFIX + card_id 

        query = super().build_query()

        response = requests.get(url, query)
        dict_response = super().convert_response_into_dict(response)

        return dict_response.get('name')


    def get_card_attachment_json(self, card_id: str) -> str:
        url = Cards.MAIN_API_PREFIX + card_id + Cards.CARDS_ATTACHMENT_SUFFIX

        query = super().build_query()

        response = requests.get(url, query)
        dict_reponse = super().convert_response_into_dict(response)

        if dict_reponse:
            return dict_reponse[0]
        else:
            return None

    def get_attachment_url_from_json(self, attachment_json: dict) -> str:
        return attachment_json.get('url')

    def build_description(self, card: Card) -> str:
        description = "## LINK \n" + card.get_link() + "\n\n" + "## DESCRIPTION \n" + card.get_description()
        return description
