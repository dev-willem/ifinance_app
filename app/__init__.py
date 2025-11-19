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
                print("Nenhuma tabela encontrada. Execute o script de inicialização se necessário.")
            
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
