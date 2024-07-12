from pydantic import BaseModel


class ShiftRequest(BaseModel):
    day: int
    type: str


class Person(BaseModel):
    name: str
    requests: list[ShiftRequest]
    bad: list[str]


class Request(BaseModel):
    year: int
    month: int
    people: list[Person]
