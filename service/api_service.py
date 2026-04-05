from data_access.user_repo import create_user
from data_access.mechanic_repo import get_mechanic
from data_access.request_repo import create_request, get_request, update_request
from data_access.escrow_repo import create_escrow, update_escrow, get_escrow
from data_access.payment_repo import record_payment
from data_access.proof_repo import save_proof, verify_proof
from core.business import build_price_breakdown, timestamp, require_proof_before_payment
from core.matching import assign_mechanic as core_assign
from core.gurantee import raise_claim as core_raise_claim


def register_user(payload):
    return create_user(payload)


def fetch_mechanic(mechanic_id):
    return get_mechanic(mechanic_id)


def create_service_request(payload):
    price = build_price_breakdown(0.0, 0.0, 0.0, 0.0)
    payload["price_breakdown"] = price
    payload["requested_at"] = timestamp()
    return create_request(payload)


def fetch_request(request_id):
    return get_request(request_id)


def assign_mechanic(request_id, payload):
    mechanic = core_assign(payload["mechanic_id"])
    if not mechanic:
        return {"error": "Mechanic not found"}
    updates = {
        "assigned_mechanic": mechanic["mechanic_id"],
        "status": "MECHANIC_ASSIGNED",
        "price_breakdown": build_price_breakdown(
            payload["price_total"],
            payload["mechanic_payout"],
            payload["platform_fee"],
            payload["assurance_fee"],
        ),
        "assigned_at": timestamp(),
    }
    return update_request(request_id, updates)


def authorize_escrow(payload):
    return create_escrow(
        {
            "request_id": payload["request_id"],
            "total_amount": payload["amount"],
            "method": payload["method"],
            "authorization_id": f"auth-{payload['request_id']}",
            "held_at": timestamp(),
        }
    )


def capture_payment(payload):
    escrow = get_escrow(payload["escrow_id"])
    if not escrow or escrow["status"] != "HELD":
        return {"error": "Escrow not available for capture"}
    payment = record_payment(
        {
            "request_id": payload["request_id"],
            "escrow_id": payload["escrow_id"],
            "amount": payload["amount"],
            "method": "ONLINE",
            "state": "CAPTURED",
            "captured_at": timestamp(),
        }
    )
    update_escrow(payload["escrow_id"], {"status": "RELEASED", "released_at": timestamp()})
    return payment


def upload_proof(payload):
    proof = save_proof(payload)
    verify_proof(proof["proof_id"])
    if require_proof_before_payment([proof]):
        update_request(payload["request_id"], {"status": "PROOF_VERIFIED"})
    return proof


def create_claim(payload):
    return core_raise_claim(payload)


def resolve_escrow(payload):
    escrow = update_escrow(payload["escrow_id"], {"status": payload["status"], "resolved_at": timestamp()})
    if payload["status"] == "REFUNDED":
        update_request(payload["request_id"], {"status": "REFUND_PROCESSED"})
    else:
        update_request(payload["request_id"], {"status": "COMPLETED"})
    return escrow
