from contextlib import nullcontext as does_not_raise
from copy import deepcopy


from models.trade import Trade
from schemas.trade import TradeFilter
from tests.fixtures.postgres.trades import TRADES

PARAMS_TEST_TRADE_SERVICE_GET_LAST_TRADING_DATES = [
    ({"limit": 10}, [Trade(**result).date for result in TRADES], does_not_raise()),
    ({"limit": 3}, [Trade(**result).date for result in TRADES[:3]], does_not_raise()),
]

PARAMS_TEST_TRADE_SERVICE_GET_DYNAMICS = [
    (
        {
            "start_date": TRADES[-1]["date"],
            "end_date": TRADES[0]["date"]
        },
        TradeFilter(
            page=None,
            per_page=None,
            like=None,
            oil_id=None,
            delivery_basis_id=None,
            delivery_type_id=None,
        ),
        TRADES,
        does_not_raise(),
    ),
    (
        {
            "start_date": TRADES[4]["date"],
            "end_date": TRADES[1]["date"],
        },
        TradeFilter(
            page=None,
            per_page=None,
            like=None,
            oil_id=None,
            delivery_basis_id=None,
            delivery_type_id=None,
        ),
        TRADES[1:5],
        does_not_raise(),
    ),
    (
        {
            "start_date": TRADES[-1]["date"],
            "end_date": TRADES[0]["date"],
        },
        TradeFilter(
            page=None,
            per_page=None,
            like=None,
            oil_id=TRADES[1]["oil_id"],
            delivery_basis_id=TRADES[1]["delivery_basis_id"],
            delivery_type_id=TRADES[1]["delivery_type_id"],
        ),
        [TRADES[1]],
        does_not_raise(),
    ),
]

PARAMS_TEST_TRADE_SERVICE_GET_TRADING_RESULTS = [
    (
        TradeFilter(
            page=None,
            per_page=None,
            like=None,
            oil_id=None,
            delivery_basis_id=None,
            delivery_type_id=None,
        ),
        TRADES,
        does_not_raise(),
    ),
    (
        TradeFilter(
            page=None,
            per_page=None,
            like=None,
            oil_id=TRADES[1]["oil_id"],
            delivery_basis_id=TRADES[1]["delivery_basis_id"],
            delivery_type_id=TRADES[1]["delivery_type_id"],
        ),
        [TRADES[1]],
        does_not_raise(),
    ),
]

PARAMS_TEST_TRADE_REPOSITORY_GET_LAST_TRADING_DATES = [
    (
        {"limit": 10},
        TRADES,
        does_not_raise(),
    ),
    (
        {"limit": 3},
        TRADES[:3],
        does_not_raise(),
    ),
]

PARAMS_TEST_TRADE_REPOSITORY_GET_DYNAMICS = deepcopy(
    PARAMS_TEST_TRADE_SERVICE_GET_DYNAMICS
)

PARAMS_TEST_TRADE_REPOSITORY_GET_TRADING_RESULTS = deepcopy(
    PARAMS_TEST_TRADE_SERVICE_GET_TRADING_RESULTS
)

PARAMS_TEST_TRADE_ROUTE_GET_LAST_TRADING_DATES = [
    (
        "api/trade/dates/?limit=10",
        {},
        200,
        [Trade(**result).date.isoformat() for result in TRADES],
        does_not_raise(),
    ),
    (
        "api/trade/dates/?limit=3",
        {},
        200,
        [Trade(**result).date.isoformat() for result in TRADES[:3]],
        does_not_raise(),
    ),
]

PARAMS_TEST_TRADE_ROUTE_GET_DYNAMICS = [
    (
        "api/trade/dynamics/",
        {},
        422,
        {},
        does_not_raise(),
    ),
    (
        "api/trade/dynamics/?start_date=2024-10-22&end_date=2024-10-25",
        {},
        200,
        [
            {
                "exchange_product_id": "DE35KGY005A",
                "exchange_product_name": "ДТ ЕВРО класс 3 (ДТ-З-К5) минус 38, НБ Когалым (самовывоз автотранспортом)",
                "oil_id": "DE35",
                "delivery_basis_id": "KGY",
                "delivery_basis_name": "НБ Когалым",
                "delivery_type_id": "A",
                "volume": "70",
                "total": "6045200",
                "count": "1",
                "date": "2024-10-25T00:00:00",
                "id": 1381,
            },
            {
                "exchange_product_id": "DE5EMTI005A",
                "exchange_product_name": "ДТ ЕВРО сорт E (ДТ-Е-К5) минус 15, НБ г. Мытищи (самовывоз автотранспортом)",
                "oil_id": "DE5E",
                "delivery_basis_id": "MTI",
                "delivery_basis_name": "НБ г. Мытищи",
                "delivery_type_id": "A",
                "volume": "50",
                "total": "3185000",
                "count": "1",
                "date": "2024-10-24T00:00:00",
                "id": 1394,
            },
            {
                "exchange_product_id": "DE5ENIL065F",
                "exchange_product_name": "ДТ ЕВРО сорт E (ДТ-Е-К5) минус 15, ст. Никель (ст. отправления)",
                "oil_id": "DE5E",
                "delivery_basis_id": "NIL",
                "delivery_basis_name": "ст. Никель",
                "delivery_type_id": "F",
                "volume": "715",
                "total": "41788500",
                "count": "8",
                "date": "2024-10-23T00:00:00",
                "id": 1409,
            },
            {
                "exchange_product_id": "A595NOV060F",
                "exchange_product_name": "Бензин (АИ-95-К5) по ГОСТ, ст. Новая Еловка (ст. отправления)",
                "oil_id": "A595",
                "delivery_basis_id": "NOV",
                "delivery_basis_name": "ст. Новая Еловка",
                "delivery_type_id": "F",
                "volume": "300",
                "total": "19110000",
                "count": "5",
                "date": "2024-10-22T00:00:00",
                "id": 1161,
            },
        ],
        does_not_raise(),
    ),
    (
        "api/trade/dynamics/?start_date=2024-10-15&end_date=2024-10-28&oil_id=DE35&delivery_basis_id=KGY&delivery_type_id=A",
        {},
        200,
        [
            {
                "exchange_product_id": "DE35KGY005A",
                "exchange_product_name": "ДТ ЕВРО класс 3 (ДТ-З-К5) минус 38, НБ Когалым (самовывоз автотранспортом)",
                "oil_id": "DE35",
                "delivery_basis_id": "KGY",
                "delivery_basis_name": "НБ Когалым",
                "delivery_type_id": "A",
                "volume": "70",
                "total": "6045200",
                "count": "1",
                "date": "2024-10-25T00:00:00",
                "id": 1381,
            }
        ],
        does_not_raise(),
    ),
]

PARAMS_TEST_TRADE_ROUTE_GET_TRADING_RESULTS = [
    (
        "api/trade/result/",
        {},
        200,
        [
            {
                "exchange_product_id": "DE18ENU005A",
                "exchange_product_name": "ДТ сорт E (ДТ-Е-К5) минус 15 по СТО 2018, Елховский НПЗ (самовывоз автотранспортом)",
                "oil_id": "DE18",
                "delivery_basis_id": "ENU",
                "delivery_basis_name": "Елховский НПЗ",
                "delivery_type_id": "A",
                "volume": "100",
                "total": "6850000",
                "count": "4",
                "date": "2024-10-28T00:00:00",
                "id": 1341,
            },
            {
                "exchange_product_id": "DE35KGY005A",
                "exchange_product_name": "ДТ ЕВРО класс 3 (ДТ-З-К5) минус 38, НБ Когалым (самовывоз автотранспортом)",
                "oil_id": "DE35",
                "delivery_basis_id": "KGY",
                "delivery_basis_name": "НБ Когалым",
                "delivery_type_id": "A",
                "volume": "70",
                "total": "6045200",
                "count": "1",
                "date": "2024-10-25T00:00:00",
                "id": 1381,
            },
            {
                "exchange_product_id": "DE5EMTI005A",
                "exchange_product_name": "ДТ ЕВРО сорт E (ДТ-Е-К5) минус 15, НБ г. Мытищи (самовывоз автотранспортом)",
                "oil_id": "DE5E",
                "delivery_basis_id": "MTI",
                "delivery_basis_name": "НБ г. Мытищи",
                "delivery_type_id": "A",
                "volume": "50",
                "total": "3185000",
                "count": "1",
                "date": "2024-10-24T00:00:00",
                "id": 1394,
            },
            {
                "exchange_product_id": "DE5ENIL065F",
                "exchange_product_name": "ДТ ЕВРО сорт E (ДТ-Е-К5) минус 15, ст. Никель (ст. отправления)",
                "oil_id": "DE5E",
                "delivery_basis_id": "NIL",
                "delivery_basis_name": "ст. Никель",
                "delivery_type_id": "F",
                "volume": "715",
                "total": "41788500",
                "count": "8",
                "date": "2024-10-23T00:00:00",
                "id": 1409,
            },
            {
                "exchange_product_id": "A595NOV060F",
                "exchange_product_name": "Бензин (АИ-95-К5) по ГОСТ, ст. Новая Еловка (ст. отправления)",
                "oil_id": "A595",
                "delivery_basis_id": "NOV",
                "delivery_basis_name": "ст. Новая Еловка",
                "delivery_type_id": "F",
                "volume": "300",
                "total": "19110000",
                "count": "5",
                "date": "2024-10-22T00:00:00",
                "id": 1161,
            },
            {
                "exchange_product_id": "DE5ESAU065F",
                "exchange_product_name": "ДТ ЕВРО сорт E (ДТ-Е-К5) минус 15, Самара-группа станций (ст. отправления)",
                "oil_id": "DE5E",
                "delivery_basis_id": "SAU",
                "delivery_basis_name": "Самара-группа станций",
                "delivery_type_id": "F",
                "volume": "1040",
                "total": "62665330",
                "count": "12",
                "date": "2024-10-21T00:00:00",
                "id": 1434,
            },
            {
                "exchange_product_id": "DE5ESTI065F",
                "exchange_product_name": "ДТ ЕВРО сорт E (ДТ-Е-К5) минус 15, ст. Стенькино II (ст. отправления)",
                "oil_id": "DE5E",
                "delivery_basis_id": "STI",
                "delivery_basis_name": "ст. Стенькино II",
                "delivery_type_id": "F",
                "volume": "650",
                "total": "39387725",
                "count": "9",
                "date": "2024-10-18T00:00:00",
                "id": 1451,
            },
            {
                "exchange_product_id": "DE5EUFM065F",
                "exchange_product_name": "ДТ ЕВРО сорт E (ДТ-Е-К5) минус 15, Уфа-группа станций (ст. отправления)",
                "oil_id": "DE5E",
                "delivery_basis_id": "UFM",
                "delivery_basis_name": "Уфа-группа станций",
                "delivery_type_id": "F",
                "volume": "2340",
                "total": "136963060",
                "count": "28",
                "date": "2024-10-17T00:00:00",
                "id": 1456,
            },
            {
                "exchange_product_id": "DE5FNVY065F",
                "exchange_product_name": "ДТ ЕВРО сорт F (ДТ-Е-К5) минус 20, ст. Новоярославская (ст. отправления)",
                "oil_id": "DE5F",
                "delivery_basis_id": "NVY",
                "delivery_basis_name": "ст. Новоярославская",
                "delivery_type_id": "F",
                "volume": "975",
                "total": "58982625",
                "count": "6",
                "date": "2024-10-16T00:00:00",
                "id": 1464,
            },
            {
                "exchange_product_id": "DE5FYAI065F",
                "exchange_product_name": "ДТ ЕВРО сорт F (ДТ-Е-К5) минус 20, ст. Яничкино (ст. отправления)",
                "oil_id": "DE5F",
                "delivery_basis_id": "YAI",
                "delivery_basis_name": "ст. Яничкино",
                "delivery_type_id": "F",
                "volume": "2015",
                "total": "121102865",
                "count": "21",
                "date": "2024-10-15T00:00:00",
                "id": 1469,
            },
        ],
        does_not_raise(),
    ),
    (
        "api/trade/result/?oil_id=DE35&delivery_basis_id=KGY&delivery_type_id=A",
        {},
        200,
        [
            {
                "exchange_product_id": "DE35KGY005A",
                "exchange_product_name": "ДТ ЕВРО класс 3 (ДТ-З-К5) минус 38, НБ Когалым (самовывоз автотранспортом)",
                "oil_id": "DE35",
                "delivery_basis_id": "KGY",
                "delivery_basis_name": "НБ Когалым",
                "delivery_type_id": "A",
                "volume": "70",
                "total": "6045200",
                "count": "1",
                "date": "2024-10-25T00:00:00",
                "id": 1381,
            }
        ],
        does_not_raise(),
    ),
]
