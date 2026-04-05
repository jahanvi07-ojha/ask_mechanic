from uuid import uuid4

_requests = {}


def create_request(payload):
    request_id = str(uuid4())
    payload.update(
        {
            "request_id": request_id,
            "status": "CREATED",
            "assigned_mechanic": None,
            "assigned_garages": [],
            "history": [],
        }
    )
    _requests[request_id] = payload
    return payload


def get_request(request_id):
    return _requests.get(request_id)


def update_request(request_id, updates):
    existing = _requests.get(request_id)
    if not existing:
        return None
    existing.update(updates)
    existing["history"].append({"updated_at": updates.get("updated_at") or "system", **updates})
    return existing
