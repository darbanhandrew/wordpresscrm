from django.contrib import admin

# Register your models here.
from woosync.models import Customer, Order


class CustomerAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
