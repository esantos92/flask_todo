from datetime import datetime
from typing import Optional # Pacote para tipos opcionais
from sqlalchemy.orm import Mapped, mapped_collumn, relationship
from sqlalchemy import String, ForeignKey, Boolean, Text
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_collumn(primary_key=True)
    email: Mapped[str] = mapped_collumn(db.String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_collumn(db.String(255))
    created_at: Mapped[datetime] = mapped_collumn(db.DateTime, default=datetime.utcnow)

    # Relationships
    todos: Mapped[list['Todo']] = relationship(back_populates='owner', cascade='all, delete')

class Todo(db.Model):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_collumn(primary_key=True)
    user_id: Mapped[int] = mapped_collumn(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    title: Mapped[str] = mapped_collumn(String(200))
    description: Mapped[Optional[str]] = mapped_collumn(Text, default=None) # Tipo opcional para descrição para ter suporte ao None
    done: Mapped[bool] = mapped_collumn(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_collumn(default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_collumn(default=None)
    # Relationships
    owner: Mapped[User] = relationship(back_populates='todos')