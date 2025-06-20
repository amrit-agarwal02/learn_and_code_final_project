import requests
from client.config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.token = None
        self.user_role = None
        self.email = None

    def set_token(self, token):
        self.token = token

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def register(self, username, email, password):
        data = {"user_name": username, "email": email, "password": password}
        resp = requests.post(f"{API_BASE_URL}/auth/register", json=data)
        return resp

    def login(self, email, password):
        data = {"email": email, "password": password}
        resp = requests.post(f"{API_BASE_URL}/auth/login", json=data)
        if resp.ok:
            self.token = resp.json()["access_token"]

            import jwt
            payload = jwt.decode(self.token, options={"verify_signature": False})
            self.user_role = payload.get("role")
            self.email = payload.get("sub")
        return resp

    def get_articles(self):
        resp = requests.get(f"{API_BASE_URL}/articles/", headers=self._headers())
        return resp

    def get_articles_by_category(self, category_id):
        resp = requests.get(f"{API_BASE_URL}/articles/?category_id={category_id}", headers=self._headers())
        return resp
