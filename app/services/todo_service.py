from datetime import datetime, timedelta
from app.domain.models import Todo
from app.repositories.todo_repo import TodoRepository
from app.extensions import db
from flask import current_app

class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo

    def list(self, user_id: int):
        return self.repo.list_by_user(user_id)

    def create(self, user_id: int, title: str, description: str = None) -> Todo:
        todo = Todo(user_id=user_id, title=title, description=description)
        return self.repo.add(todo)

    def toggle_done(self, todo: Todo) -> Todo:
        todo.done = not todo.done
        todo.completed_at = datetime.utcnow() if todo.done else None
        return self.repo.update(todo)

    def prune_completed(self) -> int:
        days = int(current_app.config['APP_PRUNE_DAYS'])
        limit = datetime.utcnow() - timedelta(days=days)
        q = db.session.query(Todo).filter(Todo.done.is_(True), Todo.completed_at < limit)
        count = q.count()
        q.delete(synchronize_session=False)
        db.session.commit()
        return count