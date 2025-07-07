from abc import ABC, abstractmethod


class IEmailService(ABC):
    
    @abstractmethod
    def send_notification_email(self, to_email: str, message: str):
        pass 