from uuid import uuid4

_users = {}


def create_user(user_payload):
    user_id = str(uuid4())
    user_payload["user_id"] = user_id
    _users[user_id] = user_payload
    return user_payload


def get_user(user_id):
    return _users.get(user_id)
