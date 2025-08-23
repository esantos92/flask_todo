from typing import Optional, Iterable
from app.domain.models import Todo
from app.extensions import db

class TodoRepository:
    def list_by_user(self, user_id: int) -> Iterable[Todo]:
        return db.session.query(Todo).filter_by(user_id=user_id).order_by(Todo.created_at.desc()).all()

    def get(self, todo_id: int, user_id: int) -> Optional[Todo]:
        return db.session.query(Todo).filter_by(id=todo_id, user_id=user_id).one_or_none()

    def add(self, todo: Todo) -> Todo:
        db.session.add(todo); db.session.commit(); return todo

    def update(self, todo: Todo) -> Todo:
        db.session.commit(); return todo

    def delete(self, todo: Todo) -> None:
        db.session.delete(todo); db.session.commit()