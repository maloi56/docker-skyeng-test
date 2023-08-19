import logging
import uuid
from datetime import timedelta

from celery import shared_task
from django.db.models import Q
from django.utils.timezone import now

from documents.models import Codereview, Document
from linter.linter import check_code
from users.models import EmailVerification, User

logger = logging.getLogger(__name__)


@shared_task(name='linter_check')
def linter_check():
    try:
        logger.info('Task started: linter_check')
        documents = Document.objects.filter(Q(status=Document.NEW) | Q(status=Document.UPDATED))
        for document in documents:
            logger.info(f'doc: linter_check: {document}')
            result = check_code(document.file.name)
            logger.info(f'linter result: {result}')
            Codereview.objects.create(document=document, review=result)
        logger.info('Task completed: linter_check')
    except Exception as e:
        logger.error(f'Error in linter_check: {e}')


@shared_task(name='send_notification_email')
def send_notification_email():
    try:
        logger.info('Task started: send_notification_email')
        reviews = Codereview.objects.filter(emailed=False, document__owner__accept_emails=True)
        for review in reviews:
            logger.info(f'review: send_notification_email: {review}')
            review.send_email_notification()
        logger.info('Task completed: send_notification_email')
    except Exception as e:
        logger.error(f'Error in send_notification_email: {e}')


@shared_task(name='send_verification_email')
def send_verification_email(user_id):
    try:
        logger.info('Task started: send_verification_email')
        user = User.objects.get(pk=user_id)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
        record.send_verification_email()
        logger.info('Task completed: send_verification_email')
    except Exception as e:
        logger.error(f'Error in send_verification_email: {e}')
