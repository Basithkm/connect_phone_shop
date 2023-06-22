from django.contrib import admin
from .models import Account

from . import models
# Register your models here.

# admin.site.register(Account)


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display =['first_name','email','phone_number','is_active','is_staff','is_admin','is_superadmin']
    list_per_page = 10
    list_filter =['is_active','is_admin','date_joined']
    search_fields =['first_name','email','phone_number']