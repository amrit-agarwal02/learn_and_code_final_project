import requests
from client.config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.token = None
        self.user_role = None
        self.user_name = None

    def set_token(self, token):
        self.token = token

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def register(self, username, email, password):
        data = {"user_name": username, "email": email, "password": password}
        response = requests.post(f"{API_BASE_URL}/auth/register", json=data)
        return response

    def login(self, email, password):
        data = {"email": email, "password": password}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=data)
        if response.ok:
            self.token = response.json()["access_token"]

            import jwt
            payload = jwt.decode(self.token, options={"verify_signature": False})
            self.user_role = payload.get("role")
            self.user_name = payload.get("user_name")
        return response

    def get_articles(self):
        response = requests.get(f"{API_BASE_URL}/articles/", headers=self._headers())
        return response

    def get_article_by_id(self, article_id):
        params = {"article_id": article_id}
        response = requests.get(f"{API_BASE_URL}/news/article/view", headers=self._headers(), params= params)
        return response

    def get_articles_by_category(self, category_id):
        response = requests.get(f"{API_BASE_URL}/articles/?category_id={category_id}", headers=self._headers())
        return response

    def get_same_day_articles(self):
        response = requests.get(f"{API_BASE_URL}/news/today_news", headers=self._headers())
        return response

    def get_articles_by_date(self, date):
        response = requests.get(f"{API_BASE_URL}/articles/?date={date}", headers=self._headers())
        return response

    def get_categories(self):
        response = requests.get(f"{API_BASE_URL}/categories/view-all", headers=self._headers())
        return response

    def save_article(self, article_id):
        data = {"article_id": article_id}
        response = requests.post(f"{API_BASE_URL}/user/article/save", json=data, headers=self._headers())
        return response

    def get_saved_articles(self):
        response = requests.get(f"{API_BASE_URL}/user/saved-articles/view", headers=self._headers())
        return response

    def delete_saved_article(self, article_id):
        data = {"article_id": article_id}
        response = requests.delete(f"{API_BASE_URL}/user/saved-articles/delete",json = data, headers=self._headers())
        return response

    def search_articles(self, params):
        params = params
        response = requests.get(f"{API_BASE_URL}/user/search", params=params, headers=self._headers())
        return response

    def get_notifications(self):
        response = requests.get(f"{API_BASE_URL}/user/notifications/view", headers=self._headers())
        return response

    def configure_notification(self, category, is_enabled, keyword = None):
        data = {"category": category, "is_enabled": is_enabled}
        if keyword:
            data["keyword"] = keyword
        response = requests.post(f"{API_BASE_URL}/user/notification/setting", json=data, headers=self._headers())
        return response

    def get_notification_setting(self):
        response = requests.get(f"{API_BASE_URL}/user/notification/settings", headers=self._headers())
        return response

    def add_keyword(self, keyword):
        data = {"keyword_name": keyword}
        response = requests.post(f"{API_BASE_URL}/users/keywords", json=data, headers=self._headers())
        return response

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

    def get_article_by_date_range(self, start_date, end_date, category_name):
        url = f"{API_BASE_URL}/user/date_range_news/{start_date}/{end_date}"
        params = {"category_name": category_name}
        response = requests.get(url, headers=self._headers(), params=params)
        return response

    def like_article(self, article_id):
        url = f"{API_BASE_URL}/feedback/like/{article_id}"
        response = requests.post(url, headers=self._headers())
        return response

    def dislike_article(self, article_id):
        url = f"{API_BASE_URL}/feedback/dislike/{article_id}"
        response = requests.post(url, headers=self._headers())
        return response

    def report_article(self, article_id, reason = None):
        url = f"{API_BASE_URL}/news/articles/{article_id}/report"
        response = requests.post(url, headers=self._headers())
        return response

    def block_article(self, article_id):
        url = f"{API_BASE_URL}/news/admin/hide/article"
        params = {"article_id": article_id}
        return requests.put(url,params = params ,headers=self._headers())

    def block_category(self, category_id):
        url = f"{API_BASE_URL}/categories/admin/category/visibility"
        params = {"category_id": category_id,
                "is_visible": False}
        return requests.put(url, params = params, headers=self._headers())

    def unblock_category(self, category_id):
        url = f"{API_BASE_URL}/categories/admin/category/visibility"
        params = {"category_id": category_id,
                "is_visible": True}
        return requests.put(url, params = params, headers=self._headers())

    def block_keyword(self, keyword):
        url = f"{API_BASE_URL}/admin/keywords/keyword/block"
        params = {
            "keyword": keyword
        }
        return requests.post(url, params= params, headers=self._headers())

    def unblock_keyword(self, keyword):
        url = f"{API_BASE_URL}/admin/keywords/keyword/unblock"
        data = {
            "keyword": keyword
        }
        return requests.delete(url, json = data, headers=self._headers())



