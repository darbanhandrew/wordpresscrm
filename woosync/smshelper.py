from .melipayamak import Api
from .models import Customer, Coupon
import re

from .woocommerce import create_coupon

username = 'gaatgallery'
password = '2488'
api = Api(username, password)


def send_sms(text, customer):
    # customer = Customer.objects.get(id=customer_id)
    if customer:
        text = text.replace("!!first_name!!", customer.billing_first_name)
        text = text.replace("!!last_name!!", customer.billing_last_name)
        text = text.replace("!!address_1!!", customer.billing_address_1)
        text = text.replace("!!city!!", customer.billing_city)
        text = text.replace("!!state!!", customer.billing_state)
        text = text.replace("!!phone!!", customer.billing_phone)
        text = text.replace("!!postcode!!", customer.billing_postcode)
        coupon_ids = re.findall(r"!!coupon_(\d+)!!", text)
        if coupon_ids:
            for coupon_id in coupon_ids:
                coupon = Coupon.objects.get(id=coupon_id)
                coupon_data = create_coupon(user_id=customer.id, coupon=coupon)
                text = text.replace("!!coupon_"+str(coupon_id)+"!!", coupon_data["code"])
        sms = api.sms()
        to = customer.billing_phone
        _from = '30008666971367'
        # text = 'تست وب سرویس ملی پیامک'
        response = sms.send(to, _from, text)
