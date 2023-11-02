from django.contrib import admin
from .models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):

    fields = (
        'email',
        'username',
        'first_name',
        'last_name',
        'role',
        'bio'
    )
    list_display = (
        'email',
        'username',
        'role',
        'is_active',
        'is_staff',
        'is_superuser'
    )
    list_editable = ("role",)
