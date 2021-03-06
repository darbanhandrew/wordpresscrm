from datetime import datetime

from woocommerce import API
from .models import Order, Customer, Coupon

wcapi = API(
    url="https://gaat.fashion",
    consumer_key="ck_53c400a337b5de4f927565e848c6dbe63c72fe25",
    consumer_secret="cs_b64df74d7c0b1f884ba617b0e03d3bc38ba47a56",
    version="wc/v3"
)


def sync_orders():
    page = 1
    while True:
        orders_query = wcapi.get("orders", params={'per_page': 100, 'page': page})
        orders = orders_query.json()
        if len(orders) == 0:
            break
        fields = ['id', 'date_created', 'date_modified', 'total', 'transaction_id', 'date_paid', 'status', 'number']
        customer_billing_fields = ['first_name', 'last_name', 'address_1', 'city', 'state', 'postcode',
                                   'country', 'email', 'phone', ]
        customer_fields = ['customer_id', 'customer_ip_address']
        for order in orders:
            if not Order.objects.filter(woo_id=order['id']):
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
                            setattr(customer, 'billing_' + customer_billing_field,
                                    order['billing'][customer_billing_field])
                else:
                    customer = Customer.objects.filter(billing_phone=order['billing']['phone']).first()
                    if not customer:
                        customer = Customer()
                        for customer_field in customer_fields:
                            setattr(customer, customer_field, order[customer_field])
                        for customer_billing_field in customer_billing_fields:
                            setattr(customer, 'billing_' + customer_billing_field,
                                    order['billing'][customer_billing_field])
                customer.save()
                django_order.customer = customer
                django_order.save()
        page = page + 1


def create_coupon(user_id, coupon: Coupon):
    code = str(user_id) + '_' + coupon.name
    data = {
        "code": code,
        "discount_type": coupon.category,
        "amount": str(coupon.discount),
    }
    if coupon.max_discount:
        data["maximum_amount"] = str(coupon.max_discount)
    if coupon.number_of_usage:
        data["usage_limit"] = coupon.number_of_usage

    return wcapi.post("coupons", data).json()
