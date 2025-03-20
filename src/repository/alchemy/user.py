from fntypes import Error
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.enums.error import UserError
from src.common.fn import from_optional
from src.db.models import UserDB
from src.repository.abstract.user import AbstractUserRepository
from src.common.types_ import UserDbResult


class AlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> UserDbResult:
        result = await self.session.execute(select(UserDB).where(UserDB.email == email))
        user = result.scalar_one_or_none()

        return from_optional(user).cast(error=UserError.not_found)

    async def create(self, email: str, hashed_password: str) -> UserDbResult:
        try:
            result = await self.session.execute(
                insert(UserDB)
                .values(email=email, password=hashed_password)
                .returning(UserDB)
            )
        except IntegrityError:
            return Error(UserError.already_exists)

        await self.session.commit()
        user = result.scalar_one_or_none()

        return from_optional(user).cast(error=UserError.cant_create)
