import logging
import sys
from datetime import datetime, timezone

from src.scheduler import UpdateScheduler

logger = logging.getLogger('debug')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[{module}][{asctime}] [Thread: {thread}] [{levelname}]:{message}', datefmt='%Y-%m-%d %H:%M:%S', style='{'))
logger.addHandler(handler)

scheduler = UpdateScheduler()
print((scheduler.run_once()-datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=timezone.utc)))
