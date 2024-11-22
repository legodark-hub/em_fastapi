from typing import Any
from schemas.trade import TradeDB, TradeFilter
from tests.fixtures import test_cases
from tests.fixtures.fake_service import FakeTradeService
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


from tests.test_utils import compare_dicts_and_db_models


@pytest.mark.asyncio(loop_scope="session")
class TestTradeService:
    class _TradeService(FakeTradeService):
        pass

    def __get_service(self, session: AsyncSession) -> FakeTradeService:
        return self._TradeService(session)

    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("values", "expected", "expectation"),
        test_cases.PARAMS_TEST_TRADE_SERVICE_GET_LAST_TRADING_DATES,
    )
    async def test_get_last_trading_dates(
        self,
        values: dict[str, Any],
        expected: list[str],
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        with expectation:
            service = self.__get_service(transaction_session)
            result = await service.get_last_trading_dates(**values)
            assert result == expected

    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("values", "filter", "expected", "expectation"),
        test_cases.PARAMS_TEST_TRADE_SERVICE_GET_DYNAMICS,
    )
    async def test_get_dynamics(
        self,
        values: dict[str, Any],
        filter: TradeFilter,
        expected: list[str],
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        with expectation:
            service = self.__get_service(transaction_session)
            result = await service.get_dynamics(**values, filter=filter)
            assert compare_dicts_and_db_models(result, expected, TradeDB)

    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("values", "expected", "expectation"),
        test_cases.PARAMS_TEST_TRADE_SERVICE_GET_TRADING_RESULTS,
    )
    async def test_get_trading_result(
        self,
        values: TradeFilter,
        expected: list[dict[str, Any]],
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        with expectation:
            service = self.__get_service(transaction_session)
            result = await service.get_trading_result(values)
            assert compare_dicts_and_db_models(result, expected, TradeDB)
