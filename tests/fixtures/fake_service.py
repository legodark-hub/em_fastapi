
from sqlalchemy.ext.asyncio import AsyncSession


from api.services.trade import TradeService
from tests.fixtures.fake_uow import FakeUnitOfWork
from utils.service import BaseService

class FakeBaseService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)


class FakeTradeService(FakeBaseService, TradeService):
    base_repository: str = "trade"