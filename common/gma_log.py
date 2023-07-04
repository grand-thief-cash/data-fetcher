from loguru import logger
from datetime import datetime


datestr = datetime.now().strftime("%Y%m%d")
logger.remove(handler_id=None)
logger.add(sink="../log/%s.log" % datestr,
           format="level={level}||time={time}||msg={message}",
           level="DEBUG",
           retention="10 days",
           rotation="1 week",
           encoding="utf-8",
           )


def logInfo(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(msg, time=now)


def logWarning(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.warning(msg, time=now)


def logError(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.error(msg, time=now)

