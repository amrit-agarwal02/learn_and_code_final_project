from abc import ABC, abstractmethod
from typing import List, Dict, Any


class INotificationService(ABC):
    
    @abstractmethod
    def save_user_notification_setting(self, user_id: int, category: str, keyword: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_user_notification_setting(self, user: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def send_unread_notifications(self) -> None:
        pass
    
    @abstractmethod
    def store_notifications(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_notification_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def update_notification_setting(self, user_id: int, setting_id: int, notification_setting: Dict[str, Any]) -> Dict[str, Any]:
        """Update user notification settings."""
        pass
    
    @abstractmethod
    def mark_notifications_as_read(self, user_id: int):
        pass 