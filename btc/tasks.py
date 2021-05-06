from core.celery import app
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from .utils import get_current_btc_exchange_rate, save_or_update_current_exchange_rate

logger = get_task_logger(__name__)


@app.task
def get_current_btc_exchange_rate_task():
    data = get_current_btc_exchange_rate()
    save_or_update_current_exchange_rate(data)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # executes every hour
    sender.add_periodic_task(
        crontab(hour="*"),
        get_current_btc_exchange_rate_task.s(),
    )
