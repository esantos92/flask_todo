from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.todo_repo import TodoRepository
from app.services.todo_service import TodoService
from app.domain.schemas import TodoIn

todos_bp = Blueprint('todos', __name__)
svc = TodoService(TodoRepository())

def get_current_user_id():
    """Helper function to get current user ID as integer"""
    user_id_str = get_jwt_identity()
    return int(user_id_str) if user_id_str else None

@todos_bp.route('', methods=['GET'])
@jwt_required()
def list_todos():
    try:
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Token inválido'}), 401
        
        todos = svc.list(user_id)
        return jsonify([{
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'completed': todo.done,
            'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
        } for todo in todos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@todos_bp.route('', methods=['POST'])
@jwt_required()
def create_todo():
    try:
        user_id = get_current_user_id()
        if not user_id:
            return jsonify({'error': 'Token inválido'}), 401
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON inválido'}), 400
        
        title = data.get('title', '').strip()
        description = data.get('description', '')
        
        if not title:
            return jsonify({'error': 'Título é obrigatório'}), 400
        
        todo = svc.create(user_id, title, description)
        return jsonify({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'completed': todo.done
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@todos_bp.route('/<int:todo_id>', methods=['PATCH'])
@jwt_required()
def toggle_todo(todo_id: int):
    """Toggle completion status of a todo"""
    user_id = get_current_user_id()
    todo = TodoRepository().get(todo_id, user_id)
    if not todo: 
        return jsonify({"msg": "Todo not found"}), 404
    
    todo = svc.toggle_done(todo)
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.done
    })

@todos_bp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id: int):
    """Update todo title and/or description"""
    user_id = get_current_user_id()
    todo = TodoRepository().get(todo_id, user_id)
    if not todo:
        return jsonify({"msg": "Todo not found"}), 404
    
    data = request.get_json()
    title = data.get('title', '').strip()
    description = data.get('description', '')
    
    if not title:
        return jsonify({'error': 'Título é obrigatório'}), 400
    
    # Atualizar através do repositório
    todo.title = title
    todo.description = description
    TodoRepository().update(todo)
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.done
    })

@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id: int):
    """Delete a todo"""
    user_id = get_current_user_id()
    todo = TodoRepository().get(todo_id, user_id)
    if not todo:
        return jsonify({"msg": "Todo not found"}), 404
    
    # Deletar através do repositório
    TodoRepository().delete(todo)
    
    return jsonify({"msg": "Todo deleted successfully"}), 200

# Manter compatibilidade com rota antiga
@todos_bp.route('/<int:todo_id>/toggle', methods=['POST'])
@jwt_required()
def toggle(todo_id: int):
    return toggle_todo(todo_id)