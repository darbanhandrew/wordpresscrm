from datetime import datetime

from woocommerce import API
from .models import Order

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
    for order in orders:
        django_order = Order()
        for field in fields:
            if field != 'id' or field != 'number' or field != 'date_created' or field != 'date_modified':
                setattr(django_order, field, order[field])
            elif field == 'date_created' or field == 'date_modified':
                datetime_object = datetime.strptime(order[field], '%Y-%m-%dT%H:%M:%S')
                setattr(django_order, field, datetime_object)
            elif field == 'id':
                setattr(django_order, 'woo_id', order[field])
            elif field == 'number':
                setattr(django_order, 'order_woo_number', order[field])
        django_order.save()
