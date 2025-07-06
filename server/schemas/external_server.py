from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExternalServerBase(BaseModel):
    server_name: str
    api_key: str
    is_active: Optional[bool] = True
    last_accessed: Optional[datetime] = None

class ExternalServerCreate(ExternalServerBase):
    pass

class UpdateServerKeyRequest(BaseModel):
    server_id: int
    updated_api_key: str