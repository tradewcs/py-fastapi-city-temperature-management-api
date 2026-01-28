from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.city import City
from schemas.city import CityCreateSchema

from .exceptions import CityAlreadyExistsException


async def get_all_cities(db: AsyncSession) -> list[City]:
    result = await db.execute(select(City))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> City | None:
    result = await db.execute(
        select(City).where(City.id == city_id)
    )
    return result.scalars().one_or_none()


async def create_city(db: AsyncSession, city_in: CityCreateSchema) -> City:
    if await db.execute(
        select(City).where(City.name == city_in.name)
    ).scalars().first():
        raise CityAlreadyExistsException(city_in.name)

    city = City(**city_in.model_dump())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city
