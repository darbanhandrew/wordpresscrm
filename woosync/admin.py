from django.contrib import admin, messages
from admin_actions.admin import ActionsModelAdmin
# Register your models here.
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from woosync.models import Customer, Order
from woosync.smshelper import send_sms
from woosync.woocommerce import sync_orders


class CustomerAdmin(ActionsModelAdmin):
    actions = ['send_sms']

    def send_sms(self, request, queryset):
        if 'apply' in request.POST:
            # The user clicked submit on the intermediate form.
            # Perform our update action:
            # queryset.update(status='NEW_STATUS')

            # Redirect to our admin view after our update has
            # completed with a nice little info message saying
            # our models have been updated:
            messages.success(request, 'SMS Sent')
            sms_text = request.POST['sms_text']
            selected_action = request.POST['_selected_action']
            for customer in queryset:
                 send_sms(sms_text, customer)
            print(selected_action)
            return HttpResponseRedirect(request.get_full_path())
        return render(request,
                      'admin/send_sms.html',
                      context={'customers': queryset})

    send_sms.short_description = "Send sms"


class OrderAdmin(ActionsModelAdmin):
    actions_list = ('sync_with_woocommerce',)

    def sync_with_woocommerce(self, request):
        sync_orders()
        return redirect(reverse_lazy('admin:woosync_order_changelist'))

    sync_with_woocommerce.short_description = 'Sync'
    sync_with_woocommerce.url_path = 'sync-with-woocommerce'


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
