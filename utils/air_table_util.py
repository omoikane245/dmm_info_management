import sys
sys.path.append('../')

import os
import requests
import json

from models.favorite_item import FavoriteItem
from utils.logger_util import LoggerUtil

class AirTableUtil(object):
    
    def __init__(self):
        self.auth_token = os.getenv("AIRTABLE_AUTH_TOKEN")
        self.fetch_favorite_item_url = os.getenv("AIRTABLE_FETCH_FAVORITE_ITEM_URL")
        self.logger = LoggerUtil().get_logger(__name__)
    
    def fetch_favorite_items(self) -> list[FavoriteItem]:
        favorite_items = []
        try:
            self.logger.info("AirTable Fetch API 実行開始")
            response = requests.get(self.fetch_favorite_item_url, headers={
                'Authorization': f'Bearer {self.auth_token}',
                'Content-type': 'application/json'
            })
            response.raise_for_status()
            result = json.loads(response.text)
            favorite_items += [
                FavoriteItem(
                    content_id = record["fields"]["content_id"],
                    site = record["fields"]["site"],
                    floor = record["fields"]["floor"],
                    service = record["fields"]["service"],
                    is_bought = bool(record["fields"]["is_bought"])
                )
                for record in result["records"]
            ]
        except Exception as e:
            self.logger.exception("AirTable接続関連エラー")
            raise e
        finally:
            self.logger.info("AirTable Fetch API 実行終了")
        
        return favorite_items