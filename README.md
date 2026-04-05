To run the code- uvicorn main:app --reload
apis and there body - POST /api/users/register
{
  "name":janvi Patel",
  "phone": "9000000000",
  "email": "janvi@example.com",
  "vehicle_details": "Honda Activa 125"
}
⮕ Response includes user_id for the next step.

GET /api/mechanics/mech-1
No body. Just confirm the mechanic data (pre-seeded in mechanic_repo).
POST /api/requests
{
  "user_id": "<use the user_id from step 1>",
  "vehicle": "Honda Activa 125",
  "issue": "Bike starts then stops",
  "coverage_packs": ["towing", "priority-support"]
}
⮕ Response includes request_id.

GET /api/requests/{request_id}
No body. Replace {request_id} with the value from step 3.
PUT /api/requests/{request_id}/assign-mechanic
{
  "mechanic_id": "mech-1",
  "price_total": 950.0,
  "mechanic_payout": 700.0,
  "platform_fee": 200.0,
  "assurance_fee": 50.0
}
⮕ Keeps the same request_id.

POST /api/escrow/authorize
{
  "request_id": "<request_id>",
  "amount": 950.0,
  "method": "ONLINE"
}
⮕ Response includes escrow_id.

POST /api/proofs
{
  "request_id": "<request_id>",
  "mechanic_id": "mech-1",
  "source": "photo",
  "uri": "s3://proofs/req-1/arrival.jpg"
}
⮕ The code auto-verifies the proof and updates the request status.

POST /api/payments/capture
{
  "request_id": "<request_id>",
  "escrow_id": "<escrow_id from step 6>",
  "amount": 950.0
}
⮕ Captures payment and releases escrow.

POST /api/claims
{
  "request_id": "<request_id>",
  "trigger": "no_show",
  "notes": "Driver waited 30 minutes, then no show"
}
POST /api/escrow/resolve
{
  "request_id": "<request_id>",
  "escrow_id": "<escrow_id>",
  "status": "RELEASED"
}
