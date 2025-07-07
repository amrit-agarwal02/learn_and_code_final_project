import requests
from client.config import API_BASE_URL

class AdminClient:
    def __init__(self, token=None):
        self.token = token

    def set_token(self, token):
        self.token = token

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def get_external_servers(self):
        response = requests.get(f"{API_BASE_URL}/external-servers/all", headers=self._headers())
        return response

    def get_external_server_details(self):
        response = requests.get(f"{API_BASE_URL}/external-servers/server-details", headers=self._headers())
        return response

    def update_external_server_api_key(self, server_id, api_key):
        data = {
            "server_id": server_id,
            "updated_api_key": api_key
        }
        response = requests.patch(f"{API_BASE_URL}/external-servers/update-server",json = data,headers=self._headers())
        return response

    def add_category(self, category_name, category_keywords):
        data = {"category_name": category_name,
                "keywords": category_keywords}
        response = requests.post(f"{API_BASE_URL}/categories/category/create", json=data, headers=self._headers())
        return response

    def block_article(self, article_id):
        url = f"{API_BASE_URL}/news/admin/hide/article"
        params = {"article_id": article_id}
        return requests.put(url, params=params, headers=self._headers())

    def block_category(self, category_id):
        url = f"{API_BASE_URL}/categories/admin/category/visibility"
        params = {"category_id": category_id,
                  "is_visible": False}
        return requests.put(url, params=params, headers=self._headers())

    def unblock_category(self, category_id):
        url = f"{API_BASE_URL}/categories/admin/category/visibility"
        params = {"category_id": category_id,
                  "is_visible": True}
        return requests.put(url, params=params, headers=self._headers())

    def block_keyword(self, keyword):
        url = f"{API_BASE_URL}/admin/keywords/keyword/block"
        params = {
            "keyword": keyword
        }
        return requests.post(url, params=params, headers=self._headers())

    def unblock_keyword(self, keyword):
        url = f"{API_BASE_URL}/admin/keywords/keyword/unblock"
        data = {
            "keyword": keyword
        }
        return requests.delete(url, json=data, headers=self._headers())
