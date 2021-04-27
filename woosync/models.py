from django.db import models

# Create your models here.
from crm import settings


class Customer(models.Model):
    customer_id = models.IntegerField(blank=True, null=True)
    # date_created = models.DateTimeField()
    # date_modified = models.DateTimeField()
    billing_first_name = models.CharField(max_length=100)
    billing_last_name = models.CharField(max_length=100)
    billing_address_1 = models.TextField(max_length=1000)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_postcode = models.CharField(max_length=100, blank=True, null=True)
    billing_country = models.CharField(max_length=100)
    billing_email = models.CharField(max_length=100, blank=True, null=True)
    billing_phone = models.CharField(max_length=100, blank=True, null=True)
    customer_ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.billing_first_name + ' ' + self.billing_last_name + ' ' + str(self.id)


class Order(models.Model):
    woo_id = models.IntegerField()
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    total = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=settings.ORDER_STATUS)
    order_woo_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return 'Order' + ' '+str(self.woo_id)
