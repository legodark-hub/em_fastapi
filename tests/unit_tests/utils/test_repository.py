from collections.abc import Sequence
from typing import Any
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.trade import Trade
from repositories.trade import TradeRepository
from schemas.trade import TradeDB, TradeFilter
from tests.fixtures import test_cases
from tests.test_utils import compare_dicts_and_db_models


@pytest.mark.asyncio(loop_scope="session")
class TestTradeRepository:
    def __get_sql_rep(self, session: AsyncSession) -> TradeRepository:
        return TradeRepository(session)

    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("values", "expected", "expectation"),
        test_cases.PARAMS_TEST_TRADE_REPOSITORY_GET_LAST_TRADING_DATES,
    )
    async def test_get_last_trading_dates(
        self,
        values: dict[str, Any],
        expected: list,
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        with expectation:
            sql_rep = self.__get_sql_rep(transaction_session)
            with expectation:
                result: Sequence[Trade] = await sql_rep.get_last_trading_dates(**values)
                assert compare_dicts_and_db_models(result, expected, TradeDB)

    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("values", "filter", "expected", "expectation"),
        test_cases.PARAMS_TEST_TRADE_REPOSITORY_GET_DYNAMICS,
    )
    async def test_get_dynamics(
        self,
        values: dict[str, Any],
        filter: TradeFilter,
        expected: list[Trade],
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        with expectation:
            result: Sequence[Trade] = await self.__get_sql_rep(
                transaction_session
            ).get_dynamics(**values, filter=filter)
            assert compare_dicts_and_db_models(result, expected, TradeDB)

    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("values", "expected", "expectation"),
        test_cases.PARAMS_TEST_TRADE_REPOSITORY_GET_TRADING_RESULTS,
    )
    async def test_get_trading_result(
        self,
        values: TradeFilter,
        expected: list[Trade],
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        with expectation:
            result: Sequence[Trade] = await self.__get_sql_rep(
                transaction_session
            ).get_trading_result(values)
            assert compare_dicts_and_db_models(result, expected, TradeDB)
