from pydantic import BaseModel
from typing import Optional

class NotificationRequest(BaseModel):
    category: str
    keyword: Optional[str] = None
    is_enabled: Optional[bool] = True

class NotificationSettingUpdate(NotificationRequest):
    is_enabled: bool