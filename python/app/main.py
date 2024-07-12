from fastapi import FastAPI
from request import Request
from makeshift import make_shift

app = FastAPI()


@app.post("/")
async def root(req: Request):
    shift = make_shift(req)
    return shift
