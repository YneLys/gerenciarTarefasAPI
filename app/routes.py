from flask import Blueprint, request, jsonify
from . import db
from .models import User, Task
from flask_jwt_extended import create_access_token, jwt_required
import bcrypt

bp = Blueprint('main', __name__)

# ---------- CADASTRO DE USUÁRIO ----------
@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Verifica se usuário já existe
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Usuário já existe"}), 400

    # Hash seguro da senha
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Usuário criado com sucesso"}), 201

# ---------- LOGIN ----------
@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)

# ---------- CRUD DE TAREFAS ----------
@bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description} for t in tasks])

@bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json()
    task = Task(title=data["title"], description=data.get("description", ""))
    db.session.add(task)
    db.session.commit()
    return jsonify({"msg": "Tarefa criada", "id": task.id}), 201

@bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    db.session.commit()
    return jsonify({"msg": "Tarefa atualizada"})

@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Tarefa removida"})
