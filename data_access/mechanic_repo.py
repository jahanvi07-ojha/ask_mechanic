from uuid import uuid4

_mechanics = {
    "mech-1": {
        "mechanic_id": "mech-1",
        "name": "Aakash Rao",
        "phone": "9000000001",
        "skills": ["engine", "bike"],
        "rating": 4.8,
        "availability": "online",
        "trust_badge": "Gold",
        "kyc_status": "VERIFIED",
    }
}


def get_mechanic(mechanic_id):
    return _mechanics.get(mechanic_id)


def list_mechanics():
    return list(_mechanics.values())


def register_mechanic(payload):
    mechanic_id = f"mech-{uuid4().hex[:6]}"
    payload["mechanic_id"] = mechanic_id
    _mechanics[mechanic_id] = payload
    return payload
