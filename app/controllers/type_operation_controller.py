from flask import Blueprint, request, jsonify
from ..models import db, TypeOperation, EntrySAC

def get_all_types():
    """Lista todos os tipos de operação"""
    try:
        types = TypeOperation.query.all()
        result = []
        for type_op in types:
            result.append({
                'id': type_op.id,
                'name': type_op.name,
                'description': type_op.description,
                'created_at': type_op.created_at.isoformat()
            })
        return jsonify({'types': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_type_by_id(type_id):
    """Busca tipo de operação por ID"""
    try:
        type_op = TypeOperation.query.get_or_404(type_id)
        return jsonify({
            'id': type_op.id,
            'name': type_op.name,
            'description': type_op.description,
            'created_at': type_op.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_operations_by_type(type_id):
    """Lista operações por tipo"""
    try:
        operations = EntrySAC.query.filter_by(type_id=type_id).all()
        result = []
        for op in operations:
            result.append({
                'id': op.id,
                'user_id': op.user_id,
                'principal_value': float(op.principal_value),
                'interest_rate': float(op.interest_rate),
                'months': op.months,
                'created_at': op.created_at.isoformat()
            })
        return jsonify({'operations': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_type():
    """Cria novo tipo de operação"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Campo obrigatório: name'}), 400
        
        type_op = TypeOperation(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(type_op)
        db.session.commit()
        
        return jsonify({
            'message': 'Tipo criado com sucesso',
            'id': type_op.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
