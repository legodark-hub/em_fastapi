from datetime import datetime
from sqlalchemy import MetaData, DateTime, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

dt_now_utc_sql = text("TIMEZONE('utc', now())")


class Base(DeclarativeBase):
    metadata = MetaData(schema="oil_trades")
    


class OilTrade(Base):
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
    created_on: Mapped[datetime] = mapped_column(
        DateTime, server_default=dt_now_utc_sql, nullable=False
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime, server_default=dt_now_utc_sql, onupdate=dt_now_utc_sql, nullable=False
    )
