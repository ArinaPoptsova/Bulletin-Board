from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from .models import Response


@receiver(post_save, sender=Response)
def send_response(sender, instance, created, **kwargs):
    if created:
        msg = EmailMultiAlternatives(
            subject=f'{instance.author.username} responsed',
            body=instance.text,
            from_email='lolkovalolka@yandex.ru',
            to=[instance.bulletin.author.email]
        )
        msg.send()
    else:
        msg = EmailMultiAlternatives(
            subject=f'Your response is accepted',
            body=f'Your response of {instance.bulletin.title} is accepted',
            from_email='lolkovalolka@yandex.ru',
            to=[instance.author.email]
        )
        msg.send()


@receiver(post_delete, sender=Response)
def send_response(sender, instance, **kwargs):
    msg = EmailMultiAlternatives(
        subject=f'Your response is deleted',
        body=f'Your response of {instance.bulletin.title} is deleted',
        from_email='lolkovalolka@yandex.ru',
        to=[instance.author.email]
    )
    msg.send()
