from datetime import datetime
from typing import TYPE_CHECKING
from collections.abc import Sequence

from fastapi import HTTPException
from pydantic import UUID4
from starlette.status import HTTP_404_NOT_FOUND

from models.trade import Trade
from schemas.trade import TradeFilter, TradeDB, TradeID, TradeResponse, TradeListResponse
from utils.service import BaseService
from utils.unit_of_work import transaction_mode

if TYPE_CHECKING:
    from collections.abc import Sequence
    
class TradeService(BaseService):
    base_repository = "trade"
    @transaction_mode
    async def get_last_trading_dates(self, limit: int) -> Sequence[datetime]:
        trades: Sequence[Trade] = await self.uow.trade.get_last_trading_dates(limit)
        return [trade.to_pydantic_schema().date for trade in trades]
    
    @transaction_mode
    async def get_dynamics(
        self, start_date: datetime, end_date: datetime, filter: TradeFilter
    ) -> Sequence[TradeDB]:
        trades: Sequence[Trade] = await self.uow.trade.get_dynamics(
            start_date, end_date, filter
        )
        return [trade.to_pydantic_schema() for trade in trades]

    @transaction_mode
    async def get_trading_result(self, filter: TradeFilter) -> Sequence[TradeDB]:
        trades: Sequence[Trade] = await self.uow.trade.get_trading_result(filter)
        return [trade.to_pydantic_schema() for trade in trades]