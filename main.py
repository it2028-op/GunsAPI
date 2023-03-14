import orjson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum


class GunRecord(BaseModel):
    name: str
    manufacturer: str
    trigger: str
    length: int
    barrel_length: int
    weight: float
    magazine: int
    url: str

    @staticmethod
    def from_dict(data: dict):
        record = GunRecord(**data)
        return record


class Problem(BaseModel):
    detail: str


class Database:
    def __init__(self):
        self._data: list = []

    def load_from_filename(self, filename: str):
        with open(filename, "rb") as f:
            data = orjson.loads(f.read())
            for record in data:
                obj = GunRecord.from_dict(record)
                self._data.append(obj)

    def delete(self, id_gun: int):
        if 0 < id_gun >= len(self._data):
            return
        self._data.pop(id_gun)

    def add(self, gun: GunRecord):
        self._data.append(gun)

    def get(self, id_gun: int):
        if 0 < id_gun >= len(self._data):
            return
        return self._data[id_gun]

    def get_all(self) -> list[GunRecord]:
        return self._data

    def update(self, id_gun: int, gun: GunRecord):
        if 0 < id_gun >= len(self._data):
            return
        self._data[id_gun] = gun

    def count(self) -> int:
        return len(self._data)


db = Database()
db.load_from_filename('guns.json')

app = FastAPI(title="Zbrojovka API", version="0.1", docs_url="/docs")

app.is_shutdown = False


@app.get("/guns", response_model=list[GunRecord])
async def get_guns():
    return db.get_all()


@app.get("/guns/{id_gun}", response_model=GunRecord)
async def get_guns(id_gun: int):
    return db.get(id_gun)


@app.get("/guns/{category}")
async def get_cat(category: Cat):
    return {"category": category}


@app.post("/guns", response_model=GunRecord)
async def post_guns(gun: GunRecord):
    db.add(gun)
    return gun


@app.delete("/guns/{id_gun}", responses={
    404: {'model': Problem}
})
async def delete_gun(id_gun: int):
    gun = db.get(id_gun)
    if gun is None:
        raise HTTPException(404, "Gun not found")
    db.delete(id_gun)
    return {'status': 'deleted'}


@app.patch("/guns/{id_gun}", responses={
    404: {'model': Problem}
})
async def update_gun(id_gun: int, updated_gun: GunRecord):
    gun = db.get(id_gun)
    if gun is None:
        raise HTTPException(404, "Gun not found")
    db.update(id_gun, updated_gun)
    return {'old': gun, 'new': updated_gun}