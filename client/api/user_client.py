import requests
import jwt
from client.config import API_BASE_URL

class UserClient:
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
        try:
            data = {"user_name": username, "email": email, "password": password}
            return requests.post(f"{API_BASE_URL}/auth/register", json=data)
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while registering user {str(e)}"}


    def login(self, email, password):
        try:
            data = {"email": email, "password": password}
            response = requests.post(f"{API_BASE_URL}/auth/login", json=data)
            if response.ok:
                self.token = response.json()["access_token"]
                payload = jwt.decode(self.token, options={"verify_signature": False})
                self.user_role = payload.get("role")
                self.user_name = payload.get("user_name")
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while login {str(e)}"}


    def get_article_by_id(self, article_id):
        try:
            params = {"article_id": article_id}
            response = requests.get(f"{API_BASE_URL}/news/article/view", headers=self._headers(), params= params)
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while fetching article by id {str(e)}"}


    def get_articles_by_category(self, category_id):
        try:
            response = requests.get(f"{API_BASE_URL}/articles/?category_id={category_id}", headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while fetching article by category {str(e)}"}


    def get_today_articles(self):
        try:
            response = requests.get(f"{API_BASE_URL}/user/today_news", headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured {str(e)}"}


    def get_categories(self):
        try:
            response = requests.get(f"{API_BASE_URL}/categories/view-all", headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while fetching categories {str(e)}"}


    def save_article(self, article_id):
        try:
            data = {"article_id": article_id}
            response = requests.post(f"{API_BASE_URL}/user/article/save", json=data, headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while saving article {str(e)}"}


    def get_saved_articles(self):
        try:
            response = requests.get(f"{API_BASE_URL}/user/saved-articles/view", headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while fetching saved articles {str(e)}"}


    def delete_saved_article(self, article_id):
        try:
            data = {"article_id": article_id}
            response = requests.delete(f"{API_BASE_URL}/user/saved-articles/delete",json = data, headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while deleting saved articles {str(e)}"}


    def search_articles(self, params):
        try:
            params = params
            response = requests.get(f"{API_BASE_URL}/user/search", params=params, headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while searching keyword {str(e)}"}


    def get_notifications(self):
        try:
            response = requests.get(f"{API_BASE_URL}/user/notifications/view", headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while fetching notifications {str(e)}"}


    def configure_notification(self, category, is_enabled, keyword = None):
        try:
            data = {"category": category, "is_enabled": is_enabled}
            if keyword:
                data["keyword"] = keyword
            response = requests.post(f"{API_BASE_URL}/user/notification/setting", json=data, headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while configuring notifications {str(e)}"}


    def get_notification_setting(self):
        try:
            response = requests.get(f"{API_BASE_URL}/user/notification/settings", headers=self._headers())
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while fetching notification setting {str(e)}"}



    def add_keyword(self, keyword):
        try:
            data = {"keyword_name": keyword}
            response = requests.post(f"{API_BASE_URL}/users/keywords", json=data, headers=self._headers())
            return response

        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while adding keyword {str(e)}"}

    def get_article_by_date_range(self, start_date, end_date, category_name):
        try:
            url = f"{API_BASE_URL}/user/date_range_news/{start_date}/{end_date}"
            params = {"category_name": category_name}
            response = requests.get(url, headers=self._headers(), params=params)
            return response

        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while fetching article {str(e)}"}

    def like_article(self, article_id):
        try:
            url = f"{API_BASE_URL}/feedback/like/{article_id}"
            response = requests.post(url, headers=self._headers())
            return response

        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while liking article {str(e)}"}

    def dislike_article(self, article_id):
        try:
            url = f"{API_BASE_URL}/feedback/dislike/{article_id}"
            response = requests.post(url, headers=self._headers())
            return response

        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while disliking article {str(e)}"}

    def report_article(self, article_id, reason=None):
        try:
            params = {"artcile_id": article_id}
            if reason is not None:
                params['reason'] = reason
            url = f"{API_BASE_URL}/news/articles/{article_id}/report"
            response = requests.post(url, headers=self._headers(), params= params)
            return response
        except requests.exceptions.ConnectionError:
            return {"error": "Server is not reachable."}
        except Exception as e:
            return {"error": f"Error occured while reporting article {str(e)}"}
