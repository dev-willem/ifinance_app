from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from ..models import db, EntrySAC, User, TypeOperation
from ..controllers import *

def login_required(f):
    """Decorator para rotas que requerem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def index():
    """Página inicial"""
    # Se o usuário estiver logado, redireciona para o dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@login_required
def dashboard():
    """Dashboard do usuário logado"""
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@login_required
def simulate():
    """Página de simulação para usuários logados"""
    user = User.query.get(session['user_id'])
    return render_template('simular.html', user=user)

@login_required
def history():
    """Página de histórico"""
    user_id = session['user_id']
    simulations = []
    try:
        # Busca simulações do usuário logado
        simulations = EntrySAC.query.filter_by(user_id=user_id).order_by(EntrySAC.created_at.desc()).all()
    except Exception as e:
        print(f"Erro ao buscar simulações: {e}")
        flash('Erro ao carregar histórico', 'error')
    
    return render_template('history/history.html', simulations=simulations)

@login_required
def profile():
    """Página de perfil do usuário"""
    user = User.query.get(session['user_id'])
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('main.dashboard'))
    
    return render_template('profile.html', user=user)

def simulate_sac():
    """Processa simulação SAC"""
    try:
        data = request.form
        
        # Validação básica
        principal_value = float(data.get('principal_value', 0))
        months = int(data.get('months', 0))
        interest_rate = float(data.get('interest_rate', 0))
        
        if not all([principal_value, months, interest_rate]):
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(url_for('main.simulate'))
        
        # Aqui você implementaria a lógica de cálculo SAC
        result = calculator_controller.sac_system_calculation(principal_value, months, interest_rate)
        print(result)
        
        # Por enquanto, apenas redirecionamos
        flash('Simulação SAC processada com sucesso!', 'success')
        return redirect(url_for('main.simulate'))
        
    except ValueError:
        flash('Valores inválidos fornecidos', 'error')
        return redirect(url_for('main.simulate'))
    except Exception as e:
        flash('Erro ao processar simulação', 'error')
        return redirect(url_for('main.simulate'))

def simulate_price():
    """Processa simulação PRICE"""
    try:
        data = request.form
        
        # Validação básica
        principal_value = float(data.get('principal_value', 0))
        months = int(data.get('months', 0))
        interest_rate = float(data.get('interest_rate', 0))
        
        if not all([principal_value, months, interest_rate]):
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(url_for('main.simulate'))
        
        # Aqui você implementaria a lógica de cálculo PRICE
        flash('Simulação PRICE processada com sucesso!', 'success')
        return redirect(url_for('main.simulate'))
        
    except ValueError:
        flash('Valores inválidos fornecidos', 'error')
        return redirect(url_for('main.simulate'))
    except Exception as e:
        flash('Erro ao processar simulação', 'error')
        return redirect(url_for('main.simulate'))

def simulate_credit():
    """Processa simulação de Crédito"""
    try:
        data = request.form
        
        # Validação básica
        principal_value = float(data.get('principal_value', 0))
        months = int(data.get('months', 0))
        interest_rate = float(data.get('interest_rate', 0))
        
        if not all([principal_value, months, interest_rate]):
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(url_for('main.simulate'))
        
        # Aqui você implementaria a lógica de cálculo de Crédito
        flash('Simulação de Crédito processada com sucesso!', 'success')
        return redirect(url_for('main.simulate'))
        
    except ValueError:
        flash('Valores inválidos fornecidos', 'error')
        return redirect(url_for('main.simulate'))
    except Exception as e:
        flash('Erro ao processar simulação', 'error')
        return redirect(url_for('main.simulate'))

def simulate_profit():
    """Processa simulação de Lucro"""
    try:
        data = request.form
        
        # Validação básica
        revenue = float(data.get('revenue', 0))
        fixed_costs = float(data.get('fixed_costs', 0))
        variable_costs = float(data.get('variable_costs', 0))
        taxes = float(data.get('taxes', 0))
        
        if not all([revenue, fixed_costs, variable_costs, taxes]):
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(url_for('main.simulate'))
        
        # Aqui você implementaria a lógica de cálculo de Lucro
        flash('Simulação de Lucro processada com sucesso!', 'success')
        return redirect(url_for('main.simulate'))
        
    except ValueError:
        flash('Valores inválidos fornecidos', 'error')
        return redirect(url_for('main.simulate'))
    except Exception as e:
        flash('Erro ao processar simulação', 'error')
        return redirect(url_for('main.simulate'))

def simulate_cet():
    """Processa simulação CET"""
    try:
        data = request.form
        
        # Validação básica
        principal_value = float(data.get('principal_value', 0))
        months = int(data.get('months', 0))
        interest_rate = float(data.get('interest_rate', 0))
        admin_fees = float(data.get('admin_fees', 0))
        insurance = float(data.get('insurance', 0))
        taxes = float(data.get('taxes', 0))
        
        if not all([principal_value, months, interest_rate, admin_fees, insurance, taxes]):
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(url_for('main.simulate'))
        
        # Aqui você implementaria a lógica de cálculo CET
        flash('Simulação CET processada com sucesso!', 'success')
        return redirect(url_for('main.simulate'))
        
    except ValueError:
        flash('Valores inválidos fornecidos', 'error')
        return redirect(url_for('main.simulate'))
    except Exception as e:
        flash('Erro ao processar simulação', 'error')
        return redirect(url_for('main.simulate'))

@login_required
def view_simulation(simulation_id):
    """Visualiza uma simulação específica"""
    try:
        simulation = EntrySAC.query.get_or_404(simulation_id)
        # Verifica se a simulação pertence ao usuário logado
        if simulation.user_id != session['user_id']:
            flash('Você não tem permissão para visualizar esta simulação', 'error')
            return redirect(url_for('main.history'))
        
        return render_template('simulation_detail.html', simulation=simulation)
    except Exception as e:
        flash('Simulação não encontrada', 'error')
        return redirect(url_for('main.history'))

@login_required
def update_profile():
    """Atualiza informações do perfil"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('main.profile'))
        
        # Atualiza dados
        user.name = request.form.get('name', user.name)
        user.email = request.form.get('email', user.email)
        user.phone = request.form.get('phone', user.phone)
        
        # Verifica se email já existe para outro usuário
        existing_user = User.query.filter(User.email == user.email, User.id != user.id).first()
        if existing_user:
            flash('Este email já está sendo usado por outro usuário', 'error')
            return redirect(url_for('main.profile'))
        
        db.session.commit()
        session['user_name'] = user.name
        session['user_email'] = user.email
        
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('main.profile'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao atualizar perfil', 'error')
        return redirect(url_for('main.profile'))

@login_required
def change_password():
    """Altera senha do usuário"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('main.profile'))
        
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verifica senha atual
        if user.password_hash != current_password:  # Em produção, usar hash
            flash('Senha atual incorreta', 'error')
            return redirect(url_for('main.profile'))
        
        # Verifica se as novas senhas coincidem
        if new_password != confirm_password:
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('main.profile'))
        
        # Atualiza senha
        user.password_hash = new_password  # Em produção, hash a senha
        db.session.commit()
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('main.profile'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao alterar senha', 'error')
        return redirect(url_for('main.profile'))

@login_required
def update_settings():
    """Atualiza configurações do usuário"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('main.profile'))
        
        # Atualiza configurações
        user.email_notifications = 'email_notifications' in request.form
        user.save_simulations = 'save_simulations' in request.form
        
        db.session.commit()
        
        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('main.profile'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao salvar configurações', 'error')
        return redirect(url_for('main.profile'))
