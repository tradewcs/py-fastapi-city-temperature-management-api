from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.temperature import Temperature
from schemas.temperature import TemperatureCreateSchema


async def get_all_temperatures(db: AsyncSession) -> list[Temperature]:
    result = await db.execute(select(Temperature))
    return result.scalars().all()


async def get_temperature_by_id(
    db: AsyncSession,
    temp_id: int
) -> Temperature | None:
    result = await db.execute(
        select(Temperature).where(Temperature.id == temp_id)
    )
    return result.scalars().one_or_none()


async def create_temperature(
    db: AsyncSession,
    temp_in: TemperatureCreateSchema
) -> Temperature:
    temp = Temperature(**temp_in.model_dump())
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp
