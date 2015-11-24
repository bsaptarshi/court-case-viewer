from __future__ import absolute_import

from celery import shared_task


@shared_task
def webScrapping(x = 0, y = 0):
    print x+y
    return x + y