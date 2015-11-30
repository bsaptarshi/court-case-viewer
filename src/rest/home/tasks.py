from __future__ import absolute_import

from celery import shared_task
from home.models import Test


@shared_task
def webScrapping():
    Test.objects.create()
    return 0