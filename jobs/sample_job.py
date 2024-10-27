import sys
sys.path.append('../')

from .abstract_job import AbstractJob
from constants.job_status import JobStatus

class SampleJob(AbstractJob):
    
    def init(self):
        self.logger.info(f"{self.get_name()} init start.")
        self.logger.info(f"{self.get_name()} init end.")
    
    def invoke(self) -> JobStatus:
        self.logger.info(f"{self.get_name()} invoke start.")
        self.logger.info(f"{self.get_name()} invoke end.")
        return JobStatus.OK
        
    def get_name(self) -> str:
        return "Job000(サンプル)"
