import requests
from client.config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.token = None
        self.user_role = None
        # self.email = None
        # self.user_id = None
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
        response = requests.get(f"{API_BASE_URL}/categories/", headers=self._headers())
        return response

    def save_article(self, article_id):
        data = {"article_id": article_id}
        response = requests.post(f"{API_BASE_URL}/users/saved-articles", json=data, headers=self._headers())
        return response

    def get_saved_articles(self):
        response = requests.get(f"{API_BASE_URL}/users/saved-articles", headers=self._headers())
        return response

    def delete_saved_article(self, saved_id):
        response = requests.delete(f"{API_BASE_URL}/users/saved-articles/{saved_id}", headers=self._headers())
        return response

    def search_articles(self, query, start_date=None, end_date=None):
        params = {"q": query}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        response = requests.get(f"{API_BASE_URL}/articles/search", params=params, headers=self._headers())
        return response

    def get_notifications(self):
        response = requests.get(f"{API_BASE_URL}/notifications/user/me", headers=self._headers())
        return response

    def configure_notification(self, category_id, is_enabled):
        data = {"category_id": category_id, "is_enabled": is_enabled}
        response = requests.post(f"{API_BASE_URL}/users/notifications/configure", json=data, headers=self._headers())
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
        response = requests.put(f"{API_BASE_URL}/admin/external-servers/{server_id}/api-key?api_key={api_key}", headers=self._headers())
        return response

    def add_category(self, category_name, category_keywords):
        data = {"category_name": category_name,
                "category_keywords": category_keywords}
        response = requests.post(f"{API_BASE_URL}/admin/category", json=data, headers=self._headers())
        return response