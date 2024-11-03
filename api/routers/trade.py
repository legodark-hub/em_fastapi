from datetime import datetime
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette.status import HTTP_200_OK

from api.services.trade import TradeService
from schemas.trade import (
    TradeDatesResponse,
    TradeFilter,
    TradeListResponse,
)


if TYPE_CHECKING:
    from models.trade import Trade


router = APIRouter(prefix="/trade")


@router.get("/dates/", status_code=HTTP_200_OK, response_model=TradeDatesResponse)
@cache()
async def get_last_trading_dates(
    limit: int,
    service: TradeService = Depends(TradeService),
) -> TradeDatesResponse:
    dates = await service.get_last_trading_dates(limit)
    return TradeDatesResponse(payload=dates)


@router.get("/dynamics/", status_code=HTTP_200_OK, response_model=TradeListResponse)
@cache()
async def get_dynamics(
    start_date: datetime,
    end_date: datetime,
    filter: TradeFilter = Depends(TradeFilter),
    service: TradeService = Depends(TradeService),
) -> TradeListResponse:
    trades = await service.get_dynamics(start_date, end_date, filter)
    return TradeListResponse(payload=trades)


@router.get("/result/", status_code=HTTP_200_OK, response_model=TradeListResponse)
@cache()
async def get_trading_result(
    filter: TradeFilter = Depends(TradeFilter),
    service: TradeService = Depends(TradeService),
) -> TradeListResponse:
    trades = await service.get_trading_result(filter)
    return TradeListResponse(payload=trades)
