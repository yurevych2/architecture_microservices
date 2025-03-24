from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI()

SECRET_TOKEN = "SECRET_TOKEN"
DB_SERVICE = "http://localhost:8001"
LOGIC_SERVICE = "http://localhost:8002"

@app.get("/")
def root():
    return {"message": "Client Service: Orchestrates calls between DB and Logic"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run_process(key: str, authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    # Get data from DB
    db_response = requests.get(f"{DB_SERVICE}/read", params={"key": key})
    if db_response.status_code != 200 or db_response.json().get("value") is None:
        raise HTTPException(status_code=404, detail="Data not found in DB")

    data = db_response.json()["value"]

    # Call Business Logic
    logic_response = requests.post(f"{LOGIC_SERVICE}/process", json={"data": data})
    processed_data = logic_response.json().get("processed_data")

    # Save to DB
    new_key = f"{key}_processed"
    requests.post(f"{DB_SERVICE}/write", json={"key": new_key, "value": processed_data})

    return {"original": data, "processed": processed_data}
