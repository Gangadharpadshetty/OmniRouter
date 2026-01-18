from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.email_validator import validate_email_or_raise

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, email: str, password: str):
        # Validate and normalize email
        normalized_email = validate_email_or_raise(email, check_mx=True, check_disposable=True)
        
        if await self.user_repo.get_by_email(normalized_email):
            raise ValueError("User already exists")

        password_hash = hash_password(password)
        return await self.user_repo.create(normalized_email, password_hash)

    async def login(self, email: str, password: str):
        # Normalize email for lookup (no MX check needed for login)
        normalized_email = validate_email_or_raise(email, check_mx=False, check_disposable=False)
        
        user = await self.user_repo.get_by_email(normalized_email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}
