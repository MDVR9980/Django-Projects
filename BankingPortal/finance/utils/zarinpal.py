from django.conf import settings
from zeep import Client


def zpal_request_handler(merchant_id, amount, detail, user_email, user_phone_number, callback):
    client = Client(settings.ZARRINPAL['gateway_request_url'])
    result = client.service.PaymenetRequest(
        merchant_id, amount, detail,
        user_email, user_phone_number, callback,
    )
    if result.Status == 100:
        return 'https://wwww.zarinpal.com/pg/StartPay/' + result.Authority, result.Authority
    else:
        return None, None


def zpal_payment_checker(merchant_id, amount, authority):
    client = Client(settings.ZARRINPAL['gateway_request_url'])
    result = client.service.PaymenetVerification(merchant_id, authority, amount)
    is_paid = True if result.Status in [100, 101] else False
    return is_paid, result.RefID
