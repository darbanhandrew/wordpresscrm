from django.contrib import admin
from admin_actions.admin import ActionsModelAdmin
# Register your models here.
from django.shortcuts import redirect
from django.urls import reverse_lazy

from woosync.models import Customer, Order
from woosync.woocommerce import sync_orders


class CustomerAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(ActionsModelAdmin):
    actions_list = ('sync_with_woocommerce',)

    def sync_with_woocommerce(self, request):
        sync_orders()
        return redirect(reverse_lazy('admin:woosync_order_changelist'))

    sync_with_woocommerce.short_description = 'Sync'
    sync_with_woocommerce.url_path = 'sync-with-woocommerce'


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
