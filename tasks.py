import os
import requests
from celery import shared_task
from celery.contrib.abortable import AbortableTask
from extensions import db


@shared_task(bind=True, base=AbortableTask)
def send_message_to_telegram(self, chat_id, text):
    url = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN')}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)


@shared_task(bind=True, base=AbortableTask)
def make_otp_expired(self, otp):
    from user.models import Otp
    otp = Otp.query.get_or_404(otp)
    otp.expired = True
    db.session.add(otp)
    db.session.commit()
    return "Otp expired successfully !"
