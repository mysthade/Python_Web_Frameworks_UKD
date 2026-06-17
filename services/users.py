from models.user import User
from schemas.user import UserCreate, UserUpdate
from services.base import BaseCRUDService, service_dependency
from utils.security import get_password_hash


class UserService(BaseCRUDService[User, UserCreate, UserUpdate]):
    model = User

    async def create(self, data: UserCreate) -> User:
        payload = data.model_dump()
        password = payload.pop("password")
        user = User(**payload, hashed_password=get_password_hash(password))
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        payload = data.model_dump(exclude_unset=True)
        if "password" in payload:
            user.hashed_password = get_password_hash(payload.pop("password"))
        for key, value in payload.items():
            setattr(user, key, value)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user


get_user_service = service_dependency(UserService)
