from django.contrib import admin

from sign.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    pass
