from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AgriFusion backend running"}

@app.post("/plan")
def plan(data: dict):
    return {"result": "Crop recommendation"}