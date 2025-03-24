from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Business Logic Service: processes data"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process")
def process(request: Request):
    data = request.json()
    input_data = data.get("data", "")
    # Simulated long-running logic
    time.sleep(2)
    processed = input_data.upper()
    return {"processed_data": processed}
