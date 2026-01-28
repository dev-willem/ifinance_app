import os
from flask import Flask
from .models import db
from .config import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    try:
        config[config_name].validate_database_config()
    except ValueError as e:
        print(f"Erro de configuração: {e}")
    
    db.init_app(app)
    register_blueprints(app)
    
    with app.app_context():
        try:
            from sqlalchemy import text
            with db.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            print("Conexão com banco de dados estabelecida com sucesso!")
            
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            if tables:
                print(f"Tabelas encontradas: {tables}")
            else:
                print("Nenhuma tabela encontrada. Criando tabelas automaticamente...")
                # Importa modelos para garantir que estão registrados no SQLAlchemy
                from .models import (
                    User, TypeOperation, EntrySAC, EntryPrice, EntryCredit,
                    EntryProfit, EntryCET, EntryFixedIncome
                )
                try:
                    db.create_all()
                    print("Tabelas criadas automaticamente com sucesso!")
                except Exception as e:
                    print(f"Falha ao criar tabelas automaticamente: {e}")

            # Garante tipos padrão quando tabelas existem
            try:
                from .models import TypeOperation
                if 'type_operations' in inspector.get_table_names():
                    if TypeOperation.query.count() == 0:
                        default_types = [
                            {
                                'name': 'Sistema de Amortização Constante (SAC)',
                                'description': 'Sistema de Amortização Constante (SAC) consiste em parcelas de valor variado que decrescem de forma constante.'
                            },
                            {
                                'name': 'PRICE',
                                'description': 'Sistema Francês de amortização (parcelas constantes).'
                            },
                            {
                                'name': 'Crédito',
                                'description': 'Simulação de operações de crédito.'
                            },
                            {
                                'name': 'Lucro',
                                'description': 'Simulação de resultado de um negócio (lucro).'
                            },
                            {
                                'name': 'CET',
                                'description': 'Custo Efetivo Total (soma de todos os custos associados).'
                            },
                            {
                                'name': 'Renda Fixa',
                                'description': 'Simulação de investimentos em renda fixa.'
                            }
                        ]
                        for type_data in default_types:
                            type_op = TypeOperation(**type_data)
                            db.session.add(type_op)
                        db.session.commit()
                        print("Tipos de operação padrão criados.")
            except Exception:
                # Se algo falhar, não interrompe a aplicação
                pass
            
        except Exception as e:
            print(f"Erro ao conectar com o banco: {e}")
            print("Verifique se o PostgreSQL está rodando e as credenciais estão corretas")
    
    return app

def register_blueprints(app):
    try:
        from .routes import register_routes
        register_routes(app)
    except ImportError as e:
        print(f"Aviso: Não foi possível importar rotas: {e}")
