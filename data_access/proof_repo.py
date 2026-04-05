from uuid import uuid4

_proofs = {}


def save_proof(payload):
    proof_id = str(uuid4())
    payload.update(
        {
            "proof_id": proof_id,
            "status": "PENDING",
        }
    )
    _proofs[proof_id] = payload
    return payload


def verify_proof(proof_id):
    proof = _proofs.get(proof_id)
    if proof:
        proof["status"] = "VERIFIED"
    return proof
