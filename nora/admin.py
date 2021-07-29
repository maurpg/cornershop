from django.contrib import admin

from nora.models import Menu, Ingredient, Profile, MenuUser, UserToken

admin.site.register(Menu)
admin.site.register(Ingredient)
admin.site.register(Profile)
admin.site.register(MenuUser)
admin.site.register(UserToken)
# Register your models here.
