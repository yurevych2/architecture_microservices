from fastapi import FastAPI, Request
from typing import Dict

app = FastAPI()

db: Dict[str, str] = {}

@app.get("/")
def root():
    return {"message": "Database Service: stores and retrieves data"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/write")
async def write(request: Request):
    body = await request.json()
    key = body.get("key")
    value = body.get("value")
    if not key or value is None:
        return {"error": "Missing key or value"}
    db[key] = value
    return {"status": "written"}

@app.get("/read")
def read(key: str):
    return {"value": db.get(key, None)}
