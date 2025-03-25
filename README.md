# FastAPI microservices

---

## Project Structure

```
microservices/
├── business_logic_service/
│   └── main.py
├── database_service/
│   └── main.py
├── client_service/
│   └── main.py
└── requirements.txt
```

---

## Flow
You should only call the Client Service. The Client Service will:
- Internally call /read on the DB.
- Internally call /process on the Business Logic Service.
- Internally call /write to save processed data.

Here’s a visual representation of what happens when a user calls ```POST /run?key=mydata``` on the Client Service:
```
User
 ↓
Client Service (8000)
 ├──→ reads "mydata" from Database Service (8001)
 ├──→ sends data to Business Logic Service (8002)
 ├──→ saves processed result to Database Service as "mydata_processed"
 ↓
Returns final response with original and processed data
```

---

## Usage

### Install requirements.txt
Navigate to ```microcervices/``` and run: 
```Terminal
pip install -r requirements.txt
```

### Run each microservice in separate terminals

```Terminal
// uvicorn business_logic_service.main:app --port 8002
uvicorn business_logic_service.main:app --host 0.0.0.0 --port 8002
uvicorn database_service.main:app --port 8001
uvicorn client_service.main:app --port 8000
```

### Sample request
In a new terminal:

1. Call client service using curl:
```Terminal
curl -X POST "http://localhost:8000/add?key=mydata&value=hello_world" -H "Authorization: Bearer SECRET_TOKEN"
```

You should see ```{"status":"written"} ```

2. Run processing pipeline:
```Terminal
curl -X POST "http://localhost:8000/run?key=mydata" -H "Authorization: Bearer SECRET_TOKEN"
```

You should see ```{"original":"hello_world","processed":"HELLO_WORLD"}```
