from dataclasses import dataclass
from datetime import datetime
from fastapi import Query
from pydantic import BaseModel

from schemas.filter import TypeFilter
from schemas.response import BaseResponse

class TradeID(BaseModel):
    id: int
    
class CreateTrade(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: str
    total: str
    count: str
    date: datetime
    
class TradeDB(TradeID, CreateTrade):
    pass

class TradeResponse(BaseResponse):
    payload: TradeDB
    
class TradeListResponse(BaseResponse):
    payload: list[TradeDB]
    
class TradeDatesResponse(BaseResponse):
    payload: list[datetime]
    
    
@dataclass
class TradeFilter(TypeFilter):
    oil_id: str | None = Query(None)
    delivery_basis_id: str | None = Query(None)
    delivery_type_id: str | None = Query(None)
 

