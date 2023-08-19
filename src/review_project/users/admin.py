from django.contrib import admin

from users.models import User


@admin.register(User)
class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
