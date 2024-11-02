from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import Result, select

from models.trade import Trade
from schemas.trade import TradeFilter
from utils.repository import SQLAlchemyRepository


class TradeRepository(SQLAlchemyRepository):
    model = Trade

    async def get_last_trading_dates(self, limit: int) -> Sequence[Trade]:
        query = (
            select(self.model)
            .distinct(self.model.date)
            .order_by(self.model.date.desc())
            .limit(limit)
        )
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def get_dynamics(
        self, start_date: datetime, end_date: datetime, filter: TradeFilter
    ) -> Sequence[Trade]:
        query = select(self.model).where(self.model.date.between(start_date, end_date))

        if filter.oil_id:
            query = query.where(self.model.oil_id == filter.oil_id)
        if filter.delivery_basis_id:
            query = query.where(
                self.model.delivery_basis_id == filter.delivery_basis_id
            )
        if filter.delivery_type_id:
            query = query.where(self.model.delivery_type_id == filter.delivery_type_id)

        if filter.limit:
            query = query.limit(filter.limit)

        if filter.offset:
            query = query.offset(filter.offset)

        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def get_trading_result(self, filter: TradeFilter) -> Sequence[Trade]:
        query = select(self.model)

        if filter.oil_id:
            query = query.where(self.model.oil_id == filter.oil_id)
        if filter.delivery_basis_id:
            query = query.where(
                self.model.delivery_basis_id == filter.delivery_basis_id
            )
        if filter.delivery_type_id:
            query = query.where(self.model.delivery_type_id == filter.delivery_type_id)

        query = query.order_by(self.model.date.desc())
        
        if filter.limit:
            query = query.limit(filter.limit)
        if filter.offset:
            query = query.offset(filter.offset)

        result: Result = await self.session.execute(query)
        return result.scalars().all()
