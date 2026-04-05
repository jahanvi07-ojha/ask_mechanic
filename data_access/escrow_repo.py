from uuid import uuid4

_escrows = {}


def create_escrow(payload):
    escrow_id = str(uuid4())
    payload.update(
        {
            "escrow_id": escrow_id,
            "status": "HELD",
        }
    )
    _escrows[escrow_id] = payload
    return payload


def get_escrow(escrow_id):
    return _escrows.get(escrow_id)


def update_escrow(escrow_id, updates):
    escrow = _escrows.get(escrow_id)
    if not escrow:
        return None
    escrow.update(updates)
    return escrow
