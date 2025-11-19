from flask import Blueprint, request, jsonify
from ..models import db, User

def get_all_users():
    """Lista todos os usuários"""
    try:
        users = User.query.all()
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            })
        return jsonify({'users': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user_by_id(user_id):
    """Busca usuário por ID"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_user(user_id):
    """Atualiza dados do usuário"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_user(user_id):
    """Deleta usuário (soft delete)"""
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
