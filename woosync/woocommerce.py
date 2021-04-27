from datetime import datetime

from woocommerce import API
from .models import Order, Customer

wcapi = API(
    url="https://gaat.fashion",
    consumer_key="ck_53c400a337b5de4f927565e848c6dbe63c72fe25",
    consumer_secret="cs_b64df74d7c0b1f884ba617b0e03d3bc38ba47a56",
    version="wc/v3"
)


def sync_orders():
    orders_query = wcapi.get("orders")
    orders = orders_query.json()
    fields = ['id', 'date_created', 'date_modified', 'total', 'transaction_id', 'date_paid', 'status', 'number']
    customer_billing_fields = ['first_name', 'last_name', 'address_1', 'city', 'state', 'postcode',
                               'country', 'email', 'phone', ]
    customer_fields = ['customer_id', 'customer_ip_address']
    for order in orders:
        django_order = Order()
        customer = Customer()
        for field in fields:
            if field != 'id' or field != 'number' or field != 'date_created' or field != 'date_modified':
                setattr(django_order, field, order[field])
            if field == 'date_created' or field == 'date_modified':
                datetime_object = datetime.strptime(order[field], '%Y-%m-%dT%H:%M:%S')
                setattr(django_order, field, datetime_object)
            if field == 'id':
                setattr(django_order, 'woo_id', order[field])
            if field == 'number':
                setattr(django_order, 'order_woo_number', order[field])
        if order['customer_id'] != 0:
            customer = Customer.objects.filter(customer_id=order['customer_id']).first()
            if not customer:
                customer = Customer()
                for customer_field in customer_fields:
                    setattr(customer, customer_field, order[customer_field])
                for customer_billing_field in customer_billing_fields:
                    setattr(customer, 'billing_' + customer_billing_field, order['billing'][customer_billing_field])
        else:
            customer = Customer.objects.filter(billing_phone=order['billing']['phone']).first()
            if not customer:
                customer = Customer()
                for customer_field in customer_fields:
                    setattr(customer, customer_field, order[customer_field])
                for customer_billing_field in customer_billing_fields:
                    setattr(customer, 'billing_' + customer_billing_field, order['billing'][customer_billing_field])
        customer.save()
        django_order.customer = customer
        django_order.save()
