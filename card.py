

class Card:

    def __init__(self, article):
        super().__init__()
        self.title = article.title
        self.link = article.link
        self.description = article.description

    def get_title(self):
        return self.title
    
    def get_link(self):
        return self.link
    
    def get_description(self):
        return self.description



