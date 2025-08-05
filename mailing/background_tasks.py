# tasks.py
import smtplib

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_verification_email(self, email, token, verification=True):
    try:
        verification_url = settings.FRONTEND_VERIFICATION_URL.format(token=token)

        subject = "Verify Your Email Address"
        text_content = f"Please verify your email: {verification_url}"

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
            reply_to=[settings.REPLY_TO_EMAIL],
        )


        html_content = render_to_string('emails/verification_email.html', {
            'verification_url': verification_url,
        })

        msg.attach_alternative(html_content, "text/html")

        # Additional headers for better deliverability
        msg.extra_headers = {
            'X-Priority': '1',
            'X-MSMail-Priority': 'High',
        }

        # Test connection before sending
        connection = msg.get_connection()
        connection.open()  # Will raise SMTPException if connection fails

        # Actually send
        msg.send()

        print(f"Email sent to {email} with token {token}")

    except smtplib.SMTPException as e:
        print(f"SMTP Error sending to {email}: {str(e)}")
        self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
    except Exception as e:
        print(f"Unexpected error sending to {email}: {str(e)}")
        self.retry(exc=e, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_password_reset_pin_email(self, email, pin):
    try:

        subject = "Your Password Reset Pin"
        text_content = f"Please verify the account belongs to you: {pin}"

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
            reply_to=[settings.REPLY_TO_EMAIL],
        )


        html_content = render_to_string('emails/password_reset_pin.html', {
            'pin': pin,
        })

        msg.attach_alternative(html_content, "text/html")

        # Additional headers for better deliverability
        msg.extra_headers = {
            'X-Priority': '1',
            'X-MSMail-Priority': 'High',
        }

        # Test connection before sending
        connection = msg.get_connection()
        connection.open()  # Will raise SMTPException if connection fails

        # Actually send
        msg.send()

        print(f"Email sent to {email} with token {token}")

    except smtplib.SMTPException as e:
        print(f"SMTP Error sending to {email}: {str(e)}")
        self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
    except Exception as e:
        print(f"Unexpected error sending to {email}: {str(e)}")
        self.retry(exc=e, countdown=60 * (2 ** self.request.retries))