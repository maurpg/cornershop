from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cornershop.celery import app
from nora.models import Menu
from nora.utils.menu_manage import MenuAction
from django.contrib.auth.models import User
from nora.utils.utils import send_email


@app.task()
def send_reminder_menu(path):
    for user in User.objects.all():
        today_menu = MenuAction()
        menus = today_menu.filter_by_date()
        return [send_email(user, menu, path) for menu in menus]
