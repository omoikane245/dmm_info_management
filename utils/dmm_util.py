import sys
sys.path.append('../')

import os
import requests

from models.item import Item
from models.favorite_item import FavoriteItem
from utils.logger_util import LoggerUtil

class DmmUtil(object):
    
    def __init__(self):
        self.api_id = os.getenv("DMM_API_ID")
        self.affiliate_id = os.getenv("DMM_AFFILIATE_ID")
        self.item_list_api_url = os.getenv("DMM_ITEM_LIST_API_URL")
        self.logger = LoggerUtil().get_logger(__name__)
    
    def fetch_items(self, not_bought_favorite_items: list[FavoriteItem]) -> list[Item]:
        items = []
        if not not_bought_favorite_items:
            return items
        
        try:
            self.logger.info("DMM.com 商品検索API ver3 実行開始")
            for item in not_bought_favorite_items:
                response = requests.get(self.item_list_api_url, params = {
                    'api_id':  self.api_id,
                    'affiliate_id': self.affiliate_id,
                    'site': item.site,
                    'service': item.service,
                    'floor': item.floor,
                    'cid': item.content_id
                })
                response.raise_for_status()

                data = response.json()
                results = data['result']['items']
                items += [
                    Item(
                        content_id = result['content_id'], 
                        title = result['title'], 
                        affiliate_url = result['affiliateURL'], 
                        sample_image_url = result['imageURL']['list'], 
                        price = result['prices']['price'], 
                        is_sale = 'campaign' in result.keys()
                    )
                    for result in results
                ]
        except Exception as e:
            self.logger.exception("DMM接続関連エラー")
            raise e
        finally:
            self.logger.info("DMM.com 商品検索API ver3 実行終了")

        return items