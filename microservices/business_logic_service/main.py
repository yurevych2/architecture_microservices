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
async def process(request: Request):
    data = await request.json()
    input_data = data.get("data", "")
    result = input_data.upper()
    return {"processed_data": result}

