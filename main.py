from fastapi import FastAPI
from handler.api_handler import router as api_router

app = FastAPI(title="Mechanic Rescue Platform")
app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"status": "Mechanic Rescue API running"}
