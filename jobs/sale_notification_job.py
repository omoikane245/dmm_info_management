import sys
sys.path.append('../')

from .abstract_job import AbstractJob
from constants.job_status import JobStatus
from utils.dmm_util import DmmUtil
from utils.air_table_util import AirTableUtil
from utils.line_util import LineUtil

from itertools import filterfalse

class SaleNotificationJob(AbstractJob):
    
    def init(self):
        self.logger.info(f"{self.get_name()} init start.")
        self.air_table_util = AirTableUtil()
        self.dmm_util = DmmUtil()
        self.line_util = LineUtil()
        self.logger.info(f"{self.get_name()} init end.")

    def invoke(self) -> JobStatus:
        self.logger.info(f"{self.get_name()} invoke start.")
        
        favorite_items = self.air_table_util.fetch_favorite_items()
        not_bought_favorite_items = list(filterfalse(lambda item : item.is_bought, favorite_items))
        items = self.dmm_util.fetch_items(not_bought_favorite_items)
        sale_items = list(filter(lambda item : item.is_sale, items))
        
        if sale_items:
            self.line_util.push_announcement(sale_items)
        else:
            self.line_util.push_disappointment_message()
        
        self.logger.info(f"{self.get_name()} invoke end.")
        return JobStatus.OK

    def get_name(self) -> str:
        return "Job001(SALE情報配信)"
