from typing import Optional
from app.domain.models import User
from app.extensions import db

class UserRepository:
    def get_by_email(self, email: str) -> Optional[User]: # self serve para indicar que é um método de instância
        return db.session.query(User).filter_by(email=email).one_or_none()