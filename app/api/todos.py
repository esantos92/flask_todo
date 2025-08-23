from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.todo_repo import TodoRepository
from app.services.todo_service import TodoService
from app.domain.schemas import TodoIn

bp = Blueprint('todos', __name__)
svc = TodoService(TodoRepository())

@bp.get('/')
@jwt_required()
def list_todos():
    user_id = get_jwt_identity()
    todos = svc.list(user_id)
    return jsonify([{
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'done': todo.done,
        'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
    } for todo in todos])

@bp.post('/')
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = TodoIn(**request.get_json())
    todo = svc.create(user_id, data.title, data.description)
    return jsonify({'id': todo.id}), 201

@bp.post('/<int:todo_id>/toggle')
@jwt_required()
def toggle(todo_id: int):
    user_id = get_jwt_identity()
    todo = TodoRepository().get(todo_id, user_id)
    if not todo: return {"msg": "Todo not found"}, 404
    todo = svc.toggle_done(todo)
    return jsonify({'done': todo.done})