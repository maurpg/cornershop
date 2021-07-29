from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cornershop.settings import EMAIL_HOST_USER
from nora.models import UserToken, MenuUser
from nora.utils.token_actions import TokenUser


def send_email(user, menu, path):
    """
    Function for send email to user, import EmailMessage from django.core.email
    param <User> user : user for send email
    param <Menu> menu : menu with information for send

    """
    token = TokenUser(user, menu)
    token_uuid = token.generate_token()
    message = render_to_string("email_reminder.html", {'menu': menu, 'token': token_uuid, 'host': path})
    mail = EmailMessage(
        subject="Menu",
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[user.email],
    )
    mail.content_subtype = "html"
    mail.send()
    return menu


def assign_menu(token):
    """
    Function for filter token , if token exist return information about
    menu, user and flag response with True Value and create instance of model
    MenuUser, this model save information about select menus of user for one date
    """
    try:
        user_token_object = UserToken.objects.get(token_user=token)
    except UserToken.DoesNotExist:
        raise Exception('Token not exist')
    menu = user_token_object.menu
    user = user_token_object.user_id
    menu_user_object = MenuUser.objects.create(user=user, menu=menu, date=menu.date_menu)
    user_token_object.delete()
    return {'menu': menu_user_object, 'response': True} if menu_user_object else {'response': False}
