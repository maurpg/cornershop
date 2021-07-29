from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cornershop.settings import EMAIL_HOST_USER


def send_email(user, menu):
    """
    Function for send email to user, import EmailMessage from django.core.email
    param <User> user : user for send email
    param <Menu> menu : menu with information for send

    """
    message = render_to_string("email_reminder.html", {'menus': menu})
    mail = EmailMessage(
        subject="Menu",
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[user.email],
    )
    mail.content_subtype = "html"
    mail.send()
    return menu