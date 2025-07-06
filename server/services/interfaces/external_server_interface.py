from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IExternalServerService(ABC):
    
    @abstractmethod
    def get_all_external_servers(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_external_server_details(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def update_server_key(self, server_id: int, new_api_key: str) -> Dict[str, Any]:
        pass 