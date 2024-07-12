from fastapi import FastAPI

# from pydantic import BaseModel

app = FastAPI()

# class ShiftRequest(BaseModel):


@app.post("/")
async def root():
    return {"message": "Hello World"}
