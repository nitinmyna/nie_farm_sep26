from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Enterprise IT Service Desk API"}