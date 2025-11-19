from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db, User

def login():
    """Página de login"""
    return render_template('auth/login.html')

def register():
    """Página de registro"""
    return render_template('auth/register.html')

def login_user():
    """Processa login do usuário"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email e senha são obrigatórios', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        # Verifica hash
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email ou senha incorretos', 'error')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        flash('Erro ao fazer login', 'error')
        return redirect(url_for('auth.login'))

def register_user():
    """Processa registro de usuário"""
    try:
        name = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        telefone = request.form.get('telefone', '')
        
        if not all([name, email, password, password2]):
            flash('Todos os campos obrigatórios devem ser preenchidos', 'error')
            return redirect(url_for('auth.register'))
        
        if password != password2:
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('auth.register'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email já cadastrado', 'error')
            return redirect(url_for('auth.register'))
        
        # 🔐 Cria hash da senha
        password_hash = generate_password_hash(password)
        
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            phone=telefone if telefone else None
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Usuário criado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao criar usuário', 'error')
        return redirect(url_for('auth.register'))

def logout_user():
    """Logout do usuário"""
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('main.index'))
    """API: Retorna dados do usuário atual"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone
    }), 200
