from logging import getLogger, StreamHandler, Formatter, INFO, Logger

class LoggerUtil(object):
    
    def get_logger(self, module: str) -> Logger:
        logger = getLogger(module)
        logger.setLevel(INFO)
        if not logger.hasHandlers():
            streamHandler = StreamHandler()
            streamHandler.setLevel(INFO)
            streamHandler.setFormatter(Formatter("%(asctime)s : %(levelname)s : %(filename)s - %(message)s"))
            logger.addHandler(streamHandler)
        return logger
