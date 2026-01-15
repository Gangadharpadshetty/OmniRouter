from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, email: str, password: str):
        if await self.user_repo.get_by_email(email):
            raise ValueError("User already exists")

        password_hash = hash_password(password)
        return await self.user_repo.create(email, password_hash)

    async def login(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}
