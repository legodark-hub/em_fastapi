from typing import Any

import pytest
from httpx import AsyncClient

from tests.fixtures import test_cases
from tests.test_utils import prepare_payload

@pytest.mark.asyncio(loop_scope="session")
class TestTradesRouter:
    @staticmethod
    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("url", "headers", "expected_status_code", "expected_payload", "expectation"),
        test_cases.PARAMS_TEST_TRADE_ROUTE_GET_LAST_TRADING_DATES,
    )
    async def test_get_last_trading_dates(
        url: str,
        headers: dict[str, Any],
        expected_status_code: int,
        expected_payload: list[str],
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response) == expected_payload

    @staticmethod
    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("url", "headers", "expected_status_code", "expected_payload", "expectation"),
        test_cases.PARAMS_TEST_TRADE_ROUTE_GET_DYNAMICS,
    )
    async def test_get_dynamics(
        url: str,
        headers: dict[str, Any],
        expected_status_code: int,
        expected_payload: list[str],
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response) == expected_payload

    @staticmethod
    @pytest.mark.usefixtures("setup_trades")
    @pytest.mark.parametrize(
        ("url", "headers", "expected_status_code", "expected_payload", "expectation"),
        test_cases.PARAMS_TEST_TRADE_ROUTE_GET_TRADING_RESULTS,
    )
    async def test_get_trading_result(
        url: str,
        headers: dict[str, Any],
        expected_status_code: int,
        expected_payload: list[str],
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response) == expected_payload
