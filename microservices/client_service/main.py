from fastapi import FastAPI, Header, HTTPException
import os
import requests
from requests.exceptions import RequestException

app = FastAPI()

SECRET_TOKEN = os.getenv("CLIENT_SECRET", "SECRET_TOKEN")
DB_SERVICE = "http://localhost:8001"
LOGIC_SERVICE = "http://localhost:8002"

@app.get("/")
def root():
    return {"message": "Client Service: Orchestrates calls between DB and Logic"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/add")
def add_data(key: str, value: str, authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    try:
        response = requests.post(f"{DB_SERVICE}/write", json={"key": key, "value": value}, timeout=3)
        response.raise_for_status()
        return response.json()
    except RequestException:
        raise HTTPException(status_code=502, detail="Failed to write to DB")

@app.post("/run")
def run_process(key: str, authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    try:
        db_response = requests.get(f"{DB_SERVICE}/read", params={"key": key}, timeout=3)
        db_response.raise_for_status()
        data = db_response.json().get("value")
        if data is None:
            raise HTTPException(status_code=404, detail="Data not found in DB")
    except RequestException:
        raise HTTPException(status_code=502, detail="Failed to read from DB")

    try:
        logic_response = requests.post(f"{LOGIC_SERVICE}/process", json={"data": data}, timeout=5)
        logic_response.raise_for_status()
        processed_data = logic_response.json().get("processed_data")
    except RequestException:
        raise HTTPException(status_code=502, detail="Failed to reach Business Logic service")

    try:
        requests.post(f"{DB_SERVICE}/write", json={"key": f"{key}_processed", "value": processed_data}, timeout=3)
    except RequestException:
        raise HTTPException(status_code=502, detail="Failed to write processed data")

    return {"original": data, "processed": processed_data}
