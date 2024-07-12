from fastapi import FastAPI
from request import Request
from makeshift import make_shift
import json

app = FastAPI()


@app.post("/")
async def root(req: Request):
    shift = make_shift(req)
    return json.loads(shift)
