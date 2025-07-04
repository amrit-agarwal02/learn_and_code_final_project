from Server.Services.blocked_keywords_service import BlockedKeywordsService

class BlockedKeywordsController:
    def __init__(self):
        self.service = BlockedKeywordsService()

    def add_keyword(self, keyword):
        return self.service.add_keyword(keyword)

    def remove_keyword(self, keyword):
        return self.service.remove_keyword(keyword)

    def get_all_keywords(self):
        return self.service.get_all_blocked_keywords()