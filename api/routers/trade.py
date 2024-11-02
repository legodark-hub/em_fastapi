from datetime import datetime
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from api.services.trade import TradeService
from schemas.trade import (
    TradeFilter,
    TradeDB,
    TradeID,
    TradeResponse,
    TradeListResponse,
)


if TYPE_CHECKING:
    from models.trade import Trade


router = APIRouter(prefix="/trade")


# @router.get("/dates/", status_code=HTTP_200_OK)
# async def get_last_trading_dates(
#     service: TradeService = Depends(TradeService),
# ) -> TradeListResponse:
#     dates = await service.get_last_trading_dates(limit=10)
#     return TradeListResponse(payload=dates)


# @router.get("/dynamics/", status_code=HTTP_200_OK)
# async def get_dynamics(
#     start_date: datetime,
#     end_date: datetime,
#     filter: TradeFilter,
#     service: TradeService = Depends(TradeService),
# ) -> TradeListResponse:
#     trades = await service.get_dynamics(start_date, end_date, filter)
#     return TradeListResponse(payload=trades)


@router.get("/result/", status_code=HTTP_200_OK)
async def get_trading_result(
    filter: TradeFilter, service: TradeService = Depends(TradeService)
) -> TradeListResponse:
    trades = await service.get_trading_result(filter)
    return TradeListResponse(payload=trades)
