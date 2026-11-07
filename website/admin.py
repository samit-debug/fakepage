
from django.contrib import admin
from .models import PlainTextUser

@admin.register(PlainTextUser)
class PlainTextUserAdmin(admin.ModelAdmin):
    # This forces the admin panel to display email and password in the list view
    list_display = ('email', 'password', 'otp_code')
