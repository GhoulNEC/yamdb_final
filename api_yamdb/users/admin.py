from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('role', 'username', 'email', 'first_name', 'last_name',
                    'bio')
    search_fields = ('role', 'username')


admin.site.register(User, UserAdmin)
