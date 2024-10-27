import sys
sys.path.append('../')

import os

from linebot import LineBotApi
from linebot.models import CarouselTemplate, CarouselColumn, URITemplateAction, TemplateSendMessage, TextSendMessage

from models.item import Item
from utils.logger_util import LoggerUtil

class LineUtil(object):
    
    def __init__(self):
        self.logger = LoggerUtil().get_logger(__name__)
        self.line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
    
    def push_announcement(self, sale_items: list[Item]):
        if not sale_items:
            return
        
        try:
            self.logger.info("LINE Messaging API プッシュ通知 実行開始")
            announcement_message = TextSendMessage(text = "SALE中の商品があります。")
            image_carousel_template_message = TemplateSendMessage(
                alt_text="お気に入り商品 SALE中",
                template=CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            thumbnail_image_url = sale_item.sample_image_url,
                            title = sale_item.title,
                            text = f"{sale_item.price} 円",
                            actions = [
                                URITemplateAction(
                                    label = "商品ページへ",
                                    uri = sale_item.affiliate_url
                                )
                            ]
                        )
                        for sale_item in sale_items
                    ]
                )
            )
            self.line_bot_api.broadcast(messages = announcement_message)
            self.line_bot_api.broadcast(messages = image_carousel_template_message)
        except Exception as e:
            self.logger.exception("LINE接続関連エラー")
            raise e
        finally:
            self.logger.info("LINE Messaging API プッシュ通知 実行終了")
    
    def push_disappointment_message(self):
        try:
            self.logger.info("LINE Messaging API プッシュ通知 実行開始")
            self.line_bot_api.broadcast(messages=TextSendMessage(text = "SALE中の商品がありませんでした。"))
        except Exception as e:
            self.logger.exception("LINE接続関連エラー")
            raise e
        finally:
            self.logger.info("LINE Messaging API プッシュ通知 実行終了")