from uuid import uuid4

_payments = {}


def record_payment(payload):
    payment_id = str(uuid4())
    payload.update({"payment_id": payment_id})
    _payments[payment_id] = payload
    return payload


def get_payment(payment_id):
    return _payments.get(payment_id)
