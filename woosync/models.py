from django.db import models

# Create your models here.
from crm import settings


class Customer(models.Model):
    woo_id = models.IntegerField()
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    billing_first_name = models.CharField(max_length=100)
    billing_last_name = models.CharField(max_length=100)
    billing_address = models.TextField(max_length=1000)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_post_code = models.CharField(max_length=100, blank=True, null=True)
    billing_country = models.CharField(max_length=100)
    billing_email = models.CharField(max_length=100, blank=True, null=True)
    billing_phone = models.CharField(max_length=100, blank=True, null=True)
    customer_ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + str(self.woo_id)


class Order(models.Model):
    woo_id = models.IntegerField()
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    total = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=settings.ORDER_STATUS)
    order_woo_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return 'Order' + ' '+str(self.woo_id)
