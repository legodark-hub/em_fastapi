from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from models.base import BaseModel
from schemas.trade import TradeDB
from utils.custom_types import created_at, updated_at

    
class Trade(BaseModel):
    __tablename__ = "spimex_trading_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[str]
    total: Mapped[str]
    count: Mapped[str]
    date: Mapped[datetime]
    created_on: Mapped[created_at]
    updated_on: Mapped[updated_at]
    
    def to_pydantic_schema(self) -> TradeDB:
        return TradeDB(**self.__dict__)