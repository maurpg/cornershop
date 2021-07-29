from django.contrib import admin

from nora.models import Menu, Ingredient, Profile, MenuUser

admin.site.register(Menu)
admin.site.register(Ingredient)
admin.site.register(Profile)
admin.site.register(MenuUser)
# Register your models here.
