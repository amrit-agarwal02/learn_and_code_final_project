from pydantic import BaseModel
from typing import Optional

class NotificationRequest(BaseModel):
    category: str
    keyword: Optional[str] = None

class NotificationSettingUpdate(NotificationRequest):
    is_enabled: bool