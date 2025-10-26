from django.contrib import admin
from .models import User, KYC
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'submitted_at')
    list_filter = ('status',)

