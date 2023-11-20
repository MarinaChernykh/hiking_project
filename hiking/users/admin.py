from django.contrib import admin

from . models import CustomUser


@admin.register(CustomUser)
class AdminRegion(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'
    )
    search_fields = ('username', 'email')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'is_staff')
