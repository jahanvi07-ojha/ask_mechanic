from uuid import uuid4

_claims = {}


def create_claim(payload):
    claim_id = str(uuid4())
    payload.update({"claim_id": claim_id, "status": "PENDING"})
    _claims[claim_id] = payload
    return payload


def resolve_claim(claim_id, resolution_notes):
    claim = _claims.get(claim_id)
    if claim:
        claim["status"] = "RESOLVED"
        claim["resolution_notes"] = resolution_notes
    return claim
