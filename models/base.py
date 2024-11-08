from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    metadata = MetaData(schema="oil_trades")
