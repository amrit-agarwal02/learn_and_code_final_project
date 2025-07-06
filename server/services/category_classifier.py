import json
from typing import Dict
import os

class CategoryClassifier:
    DEFAULT_CATEGORY = "General"

    def __init__(self, json_path: str = "D:/learn and code final project github repo/learn_and_code_final_project/server/config/category_keywords.json"):
        self.CATEGORY_KEYWORDS = self.__load_keywords(json_path)

    def __load_keywords(self, json_path: str) -> Dict[str, list]:
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Keyword file not found at path: {json_path}")

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def classify(self, title: str, description: str, content: str = "") -> str:
        text = f"{title} {description} {content}".lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return category

        return self.DEFAULT_CATEGORY