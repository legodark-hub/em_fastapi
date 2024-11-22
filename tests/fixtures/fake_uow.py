from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession


from repositories.trade import TradeRepository
from utils.unit_of_work import UnitOfWork

class FakeUnitOfWork(UnitOfWork):
    """Test class for overriding the standard UnitOfWork.
    Provides isolation using transactions at the level of a single TestCase.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def __aenter__(self) -> None:
        self.trade = TradeRepository(self._session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.flush()