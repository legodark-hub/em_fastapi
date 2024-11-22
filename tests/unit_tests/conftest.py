from collections.abc import Sequence
from copy import deepcopy

import pytest
import pytest_asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.trade import Trade
from tests.fixtures.postgres.trades import TRADES
from tests.test_utils import bulk_save_models
from utils.custom_types import AsyncFunc

@pytest_asyncio.fixture
async def setup_trades(transaction_session: AsyncSession, trades: tuple[dict]) -> None:
    await bulk_save_models(transaction_session, Trade, trades)
    
@pytest_asyncio.fixture
def get_trades(transaction_session: AsyncSession) -> AsyncFunc:
    async def _get_trades() -> Sequence[Trade]:
        result: Result = await transaction_session.execute(select(Trade))
        return result.scalars().all()
    return _get_trades

@pytest.fixture
def trades() -> list[dict]:
    return deepcopy(TRADES)