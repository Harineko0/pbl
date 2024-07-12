from fastapi import FastAPI
from request import Request
from makeshift import make_shift
import json

app = FastAPI()


@app.post("/")
async def root(req: Request):
    print(f"Request: {req}")
    shift = make_shift(req)
    res = json.loads(shift)
    print(f"Response: {res}")
    return res
