from typing import Dict, Any, List
from server.services.interfaces.external_api_interface import IExternalAPIService
from server.services.news_api_service import NewsAPIService
from server.services.the_news_api_service import TheNewsAPIService
from server.utils.logger import logger
from server.Exceptions.exceptions import ExternalServerNotFoundException

class ExternalAPIFactory:

    @staticmethod
    def create_api_service(server_name: str, api_config: Dict[str, Any]) -> IExternalAPIService:
        server_name_lower = server_name.lower()

        if "newsapi" in server_name_lower:
            logger.info(f"Creating NewsAPI service for {server_name}")
            return NewsAPIService(api_config)
        elif "thenewsapi" in server_name_lower:
            logger.info(f"Creating TheNewsAPI service for {server_name}")
            return TheNewsAPIService(api_config)
        else:
            raise ExternalServerNotFoundException(f"Unsupported external API server: {server_name}")

    @staticmethod
    def get_supported_apis() -> List[str]:
        return ["NewsAPI", "TheNewsAPI"]