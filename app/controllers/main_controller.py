from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from app import db
from ..models import db, EntrySAC, EntryPrice, EntryCredit, EntryProfit, EntryCET, EntryFixedIncome, User, TypeOperation, type_enum
from ..controllers import *


def _get_or_create_type_by_name(name, description=None):
    """Retorna instância TypeOperation existente ou cria uma nova."""
    try:
        t = TypeOperation.query.filter(TypeOperation.name.ilike(f"%{name}%")).first()
        if t:
            return t
        t = TypeOperation(name=name, description=description or name)
        db.session.add(t)
        db.session.commit()
        return t
    except Exception:
        db.session.rollback()
        # fallback: tentar buscar sem criar
        return TypeOperation.query.filter_by(name=name).first()


def _get_or_create_type_from_enum(enum_val):
    """Garante que exista um TypeOperation para o enum passado."""
    name = enum_val.name if hasattr(enum_val, 'name') else str(enum_val)
    return _get_or_create_type_by_name(name, description=name)

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
    return render_template('dashboard.html', user=user)

@login_required
def history():
    """Página de histórico"""
    user_id = session['user_id']
    simulations = []
    try:
        sims = []
        sims += EntrySAC.query.filter_by(user_id=user_id).all()
        sims += EntryPrice.query.filter_by(user_id=user_id).all()
        sims += EntryCredit.query.filter_by(user_id=user_id).all()
        sims += EntryCET.query.filter_by(user_id=user_id).all()
        sims += EntryProfit.query.filter_by(user_id=user_id).all()
        sims += EntryFixedIncome.query.filter_by(user_id=user_id).all()

        # Ordena por created_at desc
        simulations = sorted(sims, key=lambda s: getattr(s, 'created_at', None) or 0, reverse=True)
    except Exception as e:
        print(f"Erro ao buscar simulações: {e}")
        flash('Erro ao carregar histórico', 'error')
    
    return render_template('history/history.html', simulations=simulations, Type=type_enum.Type)

@login_required
def profile():
    """Página de perfil do usuário"""
    user = User.query.get(session['user_id'])
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('main.dashboard'))
    
    return render_template('profile.html', user=user)

def simulate_sac():
    try:
        data = request.form
        user_id = session.get("user_id")
        
        principal_value = float(data.get('principal_value'))
        months = int(data.get('months'))
        interest_rate = float(data.get('interest_rate'))

        tabela, total_interest, total_amount = calculator_controller.sac_system_calculation(
            principal_value, months, interest_rate
        )

        type_obj = _get_or_create_type_from_enum(type_enum.Type.SAC)
        new_sac = EntrySAC(
            user_id=user_id,
            type_id=type_obj.id if type_obj else 1,
            principal_value=principal_value,
            interest_rate=interest_rate,
            months=months,

            output_data={
                "tabela": tabela,
                "total_interest": total_interest,
                "total_amount": total_amount
            }
        )
        
        db.session.add(new_sac)
        db.session.commit()

        # Agora chama o controller
        tabela, total_interest, total_amount = calculator_controller.sac_system_calculation(
            principal_value,
            months,
            interest_rate
        )

        return render_template(
            "dashboard.html",
            tabela=[{
                "mes": row["mes"],
                "amortizacao": f"{row['amortizacao']:,.2f}",
                "juros": f"{row['juros']:,.2f}",
                "prestacao": f"{row['prestacao']:,.2f}",
                "saldo_devedor": f"{row['saldo_devedor']:,.2f}"
            } for row in tabela],
            capital_inicial=f"{principal_value:,.2f}",
            juros_totais=f"{total_interest:,.2f}",
            montante=f"{total_amount:,.2f}",
            prazo=months,
            taxa_juros=interest_rate,
            erro=None
        )

    except Exception as e:
        flash(f"Erro ao processar simulação: {e}", 'error')
        return redirect(url_for('main.simulate'))

def simulate_price():
    try:
        data = request.form
        principal_value = float(data.get('principal_value', 0))
        months = int(data.get('months', 0))
        interest_rate = float(data.get('interest_rate', 0))

        # Calcula primeiro
        tabela, total_interest, total_amount = calculator_controller.price_system_calculation(
            principal_value, months, interest_rate
        )

        user_id = session.get('user_id')
        type_obj = _get_or_create_type_from_enum(type_enum.Type.PRICE)

        new_entry = EntryPrice(
            user_id=user_id,
            type_id=type_obj.id if type_obj else 2,
            principal_value=principal_value,
            interest_rate=interest_rate,
            months=months,
            output_data={
                "tabela": tabela,
                "total_interest": total_interest,
                "total_amount": total_amount
            }
        )
        db.session.add(new_entry)
        db.session.commit()

        return render_template(
            "dashboard.html",
            tabela=[{
                "mes": row["mes"],
                "amortizacao": f"{row['amortizacao']:,.2f}",
                "juros": f"{row['juros']:,.2f}",
                "prestacao": f"{row['prestacao']:,.2f}",
                "saldo_devedor": f"{row['saldo_devedor']:,.2f}"
            } for row in tabela],
            capital_inicial=f"{principal_value:,.2f}",
            juros_totais=f"{total_interest:,.2f}",
            montante=f"{total_amount:,.2f}",
            prazo=months,
            taxa_juros=interest_rate
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao processar simulação PRICE: {e}", 'error')
        return redirect(url_for('main.simulate'))

def simulate_credit():
    try:
        data = request.form
        principal_value = float(data.get('principal_value', 0))
        months = int(data.get('months', 0))
        interest_rate = float(data.get('interest_rate', 0))

        tabela, total_interest, total_amount = calculator_controller.credit_system_calculation(
            principal_value, months, interest_rate
        )

        user_id = session.get('user_id')
        type_obj = _get_or_create_type_by_name('Crédito')

        new_entry = EntryCredit(
            user_id=user_id,
            type_id=type_obj.id if type_obj else 3,
            principal_value=principal_value,
            interest_rate=interest_rate,
            months=months,
            output_data={
                "tabela": tabela,
                "total_interest": total_interest,
                "total_amount": total_amount
            }
        )
        db.session.add(new_entry)
        db.session.commit()

        return render_template(
            "dashboard.html",
            tabela=[{
                "mes": row["mes"],
                "amortizacao": f"{row['amortizacao']:,.2f}",
                "juros": f"{row['juros']:,.2f}",
                "prestacao": f"{row['prestacao']:,.2f}",
                "saldo_devedor": f"{row['saldo_devedor']:,.2f}"
            } for row in tabela],
            capital_inicial=f"{principal_value:,.2f}",
            juros_totais=f"{total_interest:,.2f}",
            montante=f"{total_amount:,.2f}",
            prazo=months,
            taxa_juros=interest_rate
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Erro crédito: {e}", 'error')
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

        result = calculator_controller.profit_simulation(
            revenue, fixed_costs, variable_costs, taxes
        )

        # Salva a simulação de lucro
        user_id = session.get('user_id')
        # Garante existência do tipo Lucro
        type_obj = _get_or_create_type_by_name('Lucro', 'Simulação de resultado de um negócio (lucro)')
        type_id = type_obj.id if type_obj else 5
        new_entry = EntryProfit(
            user_id=user_id,
            type_id=type_id,
            revenue=revenue,
            fixed_costs=fixed_costs,
            variable_costs=variable_costs,
            taxes=taxes,
            output_data=result
        )
        db.session.add(new_entry)
        db.session.commit()

        return render_template(
            "dashboard.html",
            lucro=result,
            erro=None
        )
        
    except ValueError:
        flash('Valores inválidos fornecidos', 'error')
        return redirect(url_for('main.simulate'))
    except Exception as e:
        print(f"Erro simulate_profit: {e}")
        flash(f"Erro ao processar simulação: {e}", 'error')
        return redirect(url_for('main.simulate'))

def simulate_cet():
    try:
        data = request.form
        principal_value = float(data.get('principal_value', 0))
        months = int(data.get('months', 0))
        interest_rate = float(data.get('interest_rate', 0))
        admin_fees = float(data.get('admin_fees', 0))
        insurance = float(data.get('insurance', 0))
        taxes = float(data.get('taxes', 0))

        # Calcula antes de salvar
        tabela, total_costs, cet_percent = calculator_controller.cet_calculation(
            principal_value, months, interest_rate, admin_fees, insurance, taxes
        )

        user_id = session.get('user_id')
        type_obj = _get_or_create_type_by_name('CET')

        new_entry = EntryCET(
            user_id=user_id,
            type_id=type_obj.id if type_obj else 4,
            principal_value=principal_value,
            interest_rate=interest_rate,
            months=months,
            admin_fees=admin_fees,
            insurance=insurance,
            taxes=taxes,
            output_data={
                "tabela": tabela,
                "total_costs": total_costs,
                "cet_percent": cet_percent,
                "total_amount": principal_value + total_costs
            }
        )
        db.session.add(new_entry)
        db.session.commit()

        return render_template(
            "dashboard.html",
            tabela=[{
                "mes": row.get("mes"),
                "amortizacao": f"{row.get('amortizacao', 0):,.2f}",
                "juros": f"{row.get('juros', 0):,.2f}",
                "prestacao": f"{row.get('prestacao', 0):,.2f}",
                "saldo_devedor": f"{row.get('saldo_devedor', 0):,.2f}"
            } for row in tabela],
            capital_inicial=f"{principal_value:,.2f}",
            juros_totais=f"{total_costs:,.2f}",
            montante=f"{(principal_value + total_costs):,.2f}",
            prazo=months,
            taxa_juros=interest_rate,
            cet_percent=cet_percent
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Erro CET: {e}", 'error')
        return redirect(url_for('main.simulate'))

def destroy_simulation(simulation_id):
    """Deleta uma simulação específica"""
    try:
        simulation = None
        for Model in (EntrySAC, EntryPrice, EntryCredit, EntryCET, EntryProfit, EntryFixedIncome):
            obj = Model.query.get(simulation_id)
            if obj:
                simulation = obj
                break

        if not simulation:
            flash('Simulação não encontrada', 'error')
            return redirect(url_for('main.history'))

        # Verifica se a simulação pertence ao usuário logado
        if simulation.user_id != session['user_id']:
            flash('Você não tem permissão para deletar esta simulação', 'error')
            return redirect(url_for('main.history'))

        db.session.delete(simulation)
        db.session.commit()
        flash('Simulação deletada com sucesso!', 'success')
        return redirect(url_for('main.history'))
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar simulação', 'error')
        return redirect(url_for('main.history'))

@login_required
def view_simulation(type_id, simulation_id):
    """Visualiza uma simulação específica buscando em todos os modelos de entrada"""
    try:
        model_map = {
            type_enum.Type.SAC.value: EntrySAC,
            type_enum.Type.PRICE.value: EntryPrice,
            type_enum.Type.PROFIT.value: EntryProfit,
            type_enum.Type.CREDIT.value: EntryCredit,
            type_enum.Type.CET.value: EntryCET,
            type_enum.Type.FIXED_INCOME.value: EntryFixedIncome
        }
    
        Model = model_map.get(type_id)
        if not Model:
            flash("Tipo de simulação inválido", "error")
            return redirect(url_for('main.history'))
        
        simulation = Model.query.get(simulation_id)

        if not simulation:
            flash('Simulação não encontrada ou excluída.', 'error')
            return history()

        # O template simulation_detail.html usará simulation.output_data
        return render_template('history/details.html', simulation=simulation)

    except Exception as e:
        print(f"Erro ao visualizar simulação {simulation_id}: {e}")
        flash('Ocorreu um erro interno ao carregar os detalhes.', 'error')
        return history()

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
