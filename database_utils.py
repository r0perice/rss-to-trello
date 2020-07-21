from tinydb import TinyDB, Query

class DatabaseUtils:

    def __init__(self, database):
        self.db = database


    def if_article_in_database(self, article_url: str) -> bool:
        User = Query()
        result = self.db.search(User.article_url == article_url)
        if not result:
            return False
        else:
            return True


    def put_article_in_database(self, article_url: str):
        User = Query()
        self.db.insert({'article_url': article_url})


    def is_feed_card_in_database(self, card_id: str) -> bool:
        User = Query()
        result = self.db.search(User.card_id == card_id)
        if not result:
            return False
        else:
            return True


    def add_feed_card_in_database(self, card_id: str):
        User = Query()
        self.db.insert({'card_id': card_id})


    def delete_feed_card_from_database(self, card_id: str):
        User = Query()
        self.db.remove(User.card_id == card_id)

