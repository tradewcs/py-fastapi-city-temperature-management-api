from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base
from db.session import get_db, engine
from schemas.city import CityReadSchema, CityCreateSchema
from schemas.temperature import TemperatureReadSchema, TemperatureCreateSchema
from crud.city import get_all_cities, create_city, get_city_by_id
from crud.temperature import create_temperature, get_all_temperatures
from crud.exceptions import CityAlreadyExistsException


app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/temperatures/", response_model=TemperatureReadSchema)
async def create_temp(
    temp_in: TemperatureCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await create_temperature(db, temp_in)


@app.get("/temperatures/", response_model=list[TemperatureReadSchema])
async def read_temps(db: AsyncSession = Depends(get_db)):
    return await get_all_temperatures(db)


@app.post("/cities/", response_model=CityReadSchema)
async def create_city_endpoint(
    city_in: CityCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await create_city(db, city_in)
    except CityAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/cities/", response_model=list[CityReadSchema])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await get_all_cities(db)


@app.get("/cities/{city_id}", response_model=CityReadSchema)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_all_cities(db)
    return {"message": f"Would update temperatures for {len(cities)} cities"}
