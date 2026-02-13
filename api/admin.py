from django.contrib import admin

# Register your models here.
# crm_health/admin.py
from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'name', 
        'customer_type', 
        'created_at'
    )
