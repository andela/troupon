from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from utils import scraper


logger = get_task_logger(__name__)
# A periodic task that will run every minute (the symbol "*" means every)


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def send_periodic_emails():
    logger.info("Start task")
    result = scraper.send_periodic_emails()
    logger.info("Task finished: result = %i" % result)
