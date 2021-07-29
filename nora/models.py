from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# Create your models here.
from django.db.models import JSONField

from nora.choices import employee, nora


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('name', )

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)
    ingredient = models.ManyToManyField(Ingredient)
    date_menu = models.DateField()
    creation_date = models.DateTimeField(auto_now_add=True)


class MenuUser(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='menu', on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date')


class MenuRestrictionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient)


class Profile(models.Model):
    ROLES = (
        (nora, 'nora'),
        (employee, 'employees')
    )
    role = models.CharField(max_length=30, choices=ROLES, blank=True)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)


class UserToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    token_user = models.CharField(max_length=100)
    datetime = models.DateField(default=timezone.now)
