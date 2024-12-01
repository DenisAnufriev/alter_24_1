from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from dogs.models import Dog
from dogs.services import send_tg_message
from users.models import User


@shared_task
def send_information_about_like(email):
    """ Отправка сообщения пользователю о поставленом лайке. """
    message = "Вашей собаке поставили лайк"
    send_mail("Новый лайк", "Вашей собаке поставили лайк", EMAIL_HOST_USER, [email])
    user = User.objects.get(email=email)
    if user.tg_chat_id:
        send_tg_message(user.tg_chat_id, message)
        print("tg_send")


@shared_task
def send_email_about_birthday():
    today = timezone.now().today().date()
    print(today)
    dogs = Dog.objects.filter(owner__isnull=False, date_born=today)
    message = "Поздравляем вашу собаку с днём рождения"
    email_list = []
    for dog in dogs:
        email_list.append(dog.owner.email)
        if dog.owner.tg_chat_id:
            send_tg_message(dog.owner.tg_chat_id, message)
            print("BDAY")
    if email_list:
        send_mail(
            "Поздравление", message, EMAIL_HOST_USER, email_list
        )

    # print(today)