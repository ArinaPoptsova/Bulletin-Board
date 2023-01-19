import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from bulletins.models import Bulletin
from sign.models import User

logger = logging.getLogger(__name__)


def my_job():
    bulletins = Bulletin.objects.filter(date__gt=datetime.datetime.now(tz=None) - datetime.timedelta(days=7))
    html_content = render_to_string(
        'mailing.html',
        {
            'bulletins': bulletins
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'New bulletins',
        body=f'There are now new bulletins yet',
        from_email='lolkovalolka@yandex.ru',
        to=[user.email for user in User.objects.filter(is_active=True)]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="8", minute="00"
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
