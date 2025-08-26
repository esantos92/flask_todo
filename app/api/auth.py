from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.domain.schemas import RegisterIn, LoginIn

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/register')
def register():
    data = RegisterIn(**request.get_json())
    user = UserService(UserRepository()).register(data.email, data.password)
    return jsonify({'id': user.id, 'email': user.email}), 201

@auth_bp.post('/login')
def login():
    data = LoginIn(**request.get_json())
    user = UserService(UserRepository()).verify_credentials(data.email, data.password)
    if not user:
        return jsonify({"msg": "Bad email or password"}), 401
    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)

@auth_bp.get('/me')
@jwt_required()
def me():
    return jsonify({'user_id': get_jwt_identity()})
