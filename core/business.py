from datetime import datetime


def build_price_breakdown(total, mechanic_share, platform_fee, assurance_fee):
    return {
        "total": total,
        "mechanic_payout": mechanic_share,
        "platform_fee": platform_fee,
        "assurance_fee": assurance_fee,
    }


def require_proof_before_payment(proofs):
    return any(p.get("status") == "VERIFIED" for p in proofs)


def timestamp():
    return datetime.utcnow().isoformat()
