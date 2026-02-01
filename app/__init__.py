import os
from flask import Flask
from .models import db
from .config import config
from sqlalchemy import text, inspect

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Validação simples de config
    try:
        config[config_name].validate_database_config()
    except (ValueError, AttributeError) as e:
        app.logger.error(f"Erro de configuração: {e}")
    
    db.init_app(app)
    register_blueprints(app)
    
    with app.app_context():
        setup_database(app)
    
    return app

def setup_database(app):
    """Encapsula a lógica de inicialização do banco de dados"""
    try:
        # Testa a conexão
        db.session.execute(text('SELECT 1'))
        print("✅ Conexão com MySQL estabelecida com sucesso!")
        
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Importa modelos aqui para o SQLAlchemy "conhecê-los"
        from .models import (
            User, TypeOperation, EntrySAC, EntryPrice, EntryCredit,
            EntryProfit, EntryCET, EntryFixedIncome
        )

        if not tables:
            print("Empty DB: Criando tabelas automaticamente...")
            db.create_all()
            print("Tabelas criadas com sucesso!")
            # Atualiza a lista de tabelas após criação
            tables = inspect(db.engine).get_table_names()

        # Seed de dados iniciais (TypeOperation)
        if 'type_operations' in tables:
            seed_type_operations()

    except Exception as e:
        print(f"❌ Erro ao conectar com o banco de dados: {e}")
        print("Dica: Verifique se o MySQL está rodando e se a URL de conexão está correta.")

def seed_type_operations():
    """Popula a tabela de tipos se estiver vazia"""
    from .models import TypeOperation
    try:
        if db.session.query(TypeOperation).count() == 0:
            default_types = [
                {'name': 'SAC', 'description': 'Sistema de Amortização Constante.'},
                {'name': 'PRICE', 'description': 'Sistema Francês de amortização.'},
                {'name': 'Crédito', 'description': 'Simulação de operações de crédito.'},
                {'name': 'Lucro', 'description': 'Simulação de resultado de negócio.'},
                {'name': 'CET', 'description': 'Custo Efetivo Total.'},
                {'name': 'Renda Fixa', 'description': 'Investimentos em renda fixa.'}
            ]
            for type_data in default_types:
                db.session.add(TypeOperation(**type_data))
            db.session.commit()
            print("🌱 Dados iniciais de TypeOperation inseridos.")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao inserir sementes: {e}")

def register_blueprints(app):
    try:
        from .routes import register_routes
        register_routes(app)
    except ImportError as e:
        app.logger.warning(f"Aviso: Não foi possível importar rotas: {e}")