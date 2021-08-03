from admin_numeric_filter.admin import SliderNumericFilter, RangeNumericFilter
from django.contrib import admin, messages
from admin_actions.admin import ActionsModelAdmin
# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from woosync.models import Customer, Order, Coupon
from woosync.smshelper import send_sms
from woosync.woocommerce import sync_orders
import datetime


class CustomerOrderFilter(SimpleListFilter):
    title = 'Customer Order Behaviour'
    parameter_name = 'order__status'

    def lookups(self, request, model_admin):
        return [
            ('no_successful_orders', 'No Successful Orders'),
            ('no_order_in_last_month', 'No Order In Last Month'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'no_successful_orders':
            # orders = Order.objects.exclude(status__in=['processing', 'completed', 'shipping-progress'])
            # customer_ids = []
            # for order in orders:
            #     successful_order = Order.objects.filter(customer=order.customer,
            #                                             status__in=['processing', 'completed', 'shipping-progress'])
            #     if not successful_order:
            #         if not order.customer.id in customer_ids:
            #             customer_ids.append(order.customer.id)
            return queryset.distinct().exclude(order__status__in=['processing', 'completed', 'shipping-progress'])
        elif self.value() == 'no_order_in_last_month':
            return queryset.distinct().filter(order__date_paid__lt=datetime.date.today() - datetime.timedelta(days=30))


class OrderInline(admin.TabularInline):
    model = Order
    readonly_fields = ('woo_id', 'date_paid', 'status', 'total', 'transaction_id')


class CustomerAdmin(ActionsModelAdmin):
    actions = ['send_sms']

    def send_sms(self, request, queryset):
        coupons = Coupon.objects.all()
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
                      context={'customers': queryset, 'coupons': coupons})

    send_sms.short_description = "Send sms"
    actions_list = ('calculate_loyalty',)
    inlines = (OrderInline,)

    def calculate_loyalty(self, request):
        customers = Customer.objects.all()
        for customer in customers:
            orders = Order.objects.filter(customer=customer)
            customer.number_of_successful_orders = len(
                Order.objects.filter(customer=customer, status__in=['processing', 'completed', 'shipping-progress']))
            customer.number_of_failed_orders = len(orders) \
                                               - customer.number_of_successful_orders
            month_orders = orders.filter(date_paid__lt=datetime.date.today() - datetime.timedelta(days=30),
                                         status__in=['processing', 'completed', 'shipping-progress']).all()
            orders = orders.filter(status__in=['processing', 'completed', 'shipping-progress']).all()
            if orders:
                customer.total_bought = 0
                for order in orders:
                    customer.total_bought += order.total
            if month_orders:
                total_number = 1
                customer.mean_month_bought = 0
                for month_order in month_orders:
                    customer.mean_month_bought = ((
                                                          total_number - 1) * customer.mean_month_bought + month_order.total) / total_number
            customer.save()
        return redirect(reverse_lazy('admin:woosync_customer_changelist'))

    calculate_loyalty.short_description = 'Calculate Loyalty'
    calculate_loyalty.url_path = 'calculate-loyalty'
    list_filter = (CustomerOrderFilter, ('number_of_successful_orders', RangeNumericFilter))
    list_display = ('id', '__str__', 'billing_first_name', 'billing_last_name', 'number_of_successful_orders',)
    ordering = ('number_of_successful_orders',)
    readonly_fields = ('number_of_successful_orders',)


class OrderAdmin(ActionsModelAdmin):
    actions_list = ('sync_with_woocommerce',)

    def sync_with_woocommerce(self, request):
        sync_orders()
        return redirect(reverse_lazy('admin:woosync_order_changelist'))

    sync_with_woocommerce.short_description = 'Sync'
    sync_with_woocommerce.url_path = 'sync-with-woocommerce'


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon)
