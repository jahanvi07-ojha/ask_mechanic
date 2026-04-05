from data_access.claim_repo import create_claim as persist_claim, resolve_claim


def raise_claim(payload):
    return persist_claim(payload)


def settle_claim(claim_id, notes):
    return resolve_claim(claim_id, notes)
