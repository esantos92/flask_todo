from app.extensions import bcrypt
from app.domain.models import User
from app.repositories.user_repo import UserRepository
from app.infra.email import send_welcome_email

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, email: str, password: str) -> User:
        if self.repo.get_by_email(email):
            raise ValueError("Email already registered")
        pw_hash = bcrypt.generate_password_hash(password).decode()
        user = User(email=email, password_hash=pw_hash)
        self.repo.add(user)
        send_welcome_email.delay(email) # Asynchronous background Celery task to send email
        return user

    def verify_credentials(self, email: str, password: str) -> User | None:
        user = self.repo.get_by_email(email)
        if bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None