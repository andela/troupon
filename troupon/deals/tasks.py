from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from utils import scraper

logger = get_task_logger(__name__)


# A periodic task that will run every minute
@periodic_task(run_every=(crontab(hour=10, day_of_week="Wednesday")))
def send_periodic_emails():
    logger.info("Start task")
    result = scraper.send_periodic_emails()
    logger.info("Task finished: result = %i" % result)
