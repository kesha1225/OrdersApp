import abc

from src.common.types_ import UserDbResult


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_email(self, email: str) -> UserDbResult: ...

    @abc.abstractmethod
    async def create(self, email: str, hashed_password: str) -> UserDbResult: ...
