from celery import shared_task
from django.core.mail import send_mail
from .models import Reservation

@shared_task
def send_confirmation_email(reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    subject = 'Reservation Confirmation'
    message = f'Hi {reservation.name}, your reservation for room {reservation.room.name} is confirmed from {reservation.start_time} to {reservation.end_time}.'
    from_email = 'test@example.com'
    recipient_list = [reservation.email]
    send_mail(subject, message, from_email, recipient_list)