from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdminCustom(UserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'last_name',
                'email',
                'password',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_employee'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'last_name',
                'email',
                'password',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_employee'
            ),
        }),
    )
    list_display = (
        'id',
        'last_name',
        'email',
        'is_active',
    )

    list_filter = ()
    search_fields = ('email',)
    ordering = ('id',)