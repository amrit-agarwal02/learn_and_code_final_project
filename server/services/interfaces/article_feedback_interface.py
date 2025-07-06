from abc import ABC, abstractmethod
from typing import Dict, Any


class IArticleFeedbackService(ABC):
    
    @abstractmethod
    def like_article(self, user_id: int, article_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def dislike_article(self, user_id: int, article_id: int) -> Dict[str, Any]:
        pass 