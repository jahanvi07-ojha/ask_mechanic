from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from service.api_service import (
    register_user,
    fetch_mechanic,
    create_service_request,
    fetch_request,
    assign_mechanic,
    authorize_escrow,
    capture_payment,
    upload_proof,
    create_claim,
    resolve_escrow,
)

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str]
    vehicle_details: str


class RequestCreate(BaseModel):
    user_id: str
    vehicle: str
    issue: str
    coverage_packs: Optional[List[str]] = []


class AssignPayload(BaseModel):
    mechanic_id: str
    price_total: float
    mechanic_payout: float
    platform_fee: float
    assurance_fee: float


class EscrowPayload(BaseModel):
    request_id: str
    amount: float
    method: str


class PaymentCapture(BaseModel):
    request_id: str
    escrow_id: str
    amount: float


class ProofUpload(BaseModel):
    request_id: str
    mechanic_id: str
    source: str
    uri: str


class ClaimCreate(BaseModel):
    request_id: str
    trigger: str
    notes: Optional[str]


class EscrowResolve(BaseModel):
    request_id: str
    escrow_id: str
    status: str  # RELEASED or REFUNDED


@router.post("/users/register")
def api_register_user(payload: UserCreate):
    return register_user(payload.dict())


@router.get("/mechanics/{mechanic_id}")
def api_fetch_mechanic(mechanic_id: str):
    mechanic = fetch_mechanic(mechanic_id)
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return mechanic


@router.post("/requests")
def api_create_request(payload: RequestCreate):
    return create_service_request(payload.dict())


@router.get("/requests/{request_id}")
def api_fetch_request(request_id: str):
    request = fetch_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.put("/requests/{request_id}/assign-mechanic")
def api_assign_mechanic(request_id: str, payload: AssignPayload):
    return assign_mechanic(request_id, payload.dict())


@router.post("/escrow/authorize")
def api_authorize_escrow(payload: EscrowPayload):
    return authorize_escrow(payload.dict())


@router.post("/payments/capture")
def api_capture_payment(payload: PaymentCapture):
    return capture_payment(payload.dict())


@router.post("/proofs")
def api_upload_proof(payload: ProofUpload):
    return upload_proof(payload.dict())


@router.post("/claims")
def api_create_claim(payload: ClaimCreate):
    return create_claim(payload.dict())


@router.post("/escrow/resolve")
def api_resolve_escrow(payload: EscrowResolve):
    return resolve_escrow(payload.dict())
