import sys
sys.path.append('../')

from constants.job_status import JobStatus
from utils.logger_util import LoggerUtil

from abc import ABCMeta, abstractmethod

class AbstractJob(metaclass=ABCMeta):
    
    def __init__(self):
        self.logger = LoggerUtil().get_logger(__name__)
    
    def execute(self) -> JobStatus:
        result = JobStatus.NG
        try:
            self.logger.info(f"{self.get_name()} start.")
            self.init()
            result = self.invoke()
        except:
            self.logger.exception(f"{self.get_name()} error.")
        finally:
            self.logger.info(f"{self.get_name()} end. status={result.name}")
        return result
    
    @abstractmethod
    def init(self):
        pass
    
    @abstractmethod
    def invoke(self) -> JobStatus:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
