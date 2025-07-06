from server.repositories.blocked_keywords_repo import BlockedKeywordsRepo

class BlockedKeywordsService:
    def __init__(self):
        self.repo = BlockedKeywordsRepo()

    def add_keyword(self, keyword):
        return self.repo.add_keyword(keyword)

    def remove_keyword(self, keyword):
        return self.repo.remove_keyword(keyword)

    def get_all_blocked_keywords(self):
        return self.repo.get_all_blocked_keywords()