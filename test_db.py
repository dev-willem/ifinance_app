import os
import sys
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    print("Testando conexão com o banco de dados...")
    print("=" * 50)
    
    try:
        from app import create_app
        
        print("Importações realizadas com sucesso")
        
        app = create_app()
        
        from app.models import db
        
        with app.app_context():
            print("\nVerificando conexão e tabelas existentes...")
            
            from sqlalchemy import text
            with db.engine.connect() as connection:
                result = connection.execute(text('SELECT version()'))
                version = result.fetchone()[0]
                print(f"Conexão estabelecida com PostgreSQL: {version[:50]}...")
            
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"Tabelas encontradas: {tables}")
                
                expected_tables = ['users', 'type_operations', 'entry_sac', 'entry_price', 'entry_credit', 'entry_profit', 'entry_cet', 'entry_fixed_income']
                existing_expected = [table for table in expected_tables if table in tables]
                missing_tables = [table for table in expected_tables if table not in tables]
                
                if existing_expected:
                    print(f"Tabelas do sistema encontradas: {existing_expected}")
                
                if missing_tables:
                    print(f"Tabelas do sistema não encontradas: {missing_tables}")
                    print("Para criar as tabelas, execute: python init_db.py")
            else:
                print("Nenhuma tabela encontrada no banco.")
                print("Para criar as tabelas do sistema, execute: python init_db.py")
            
            print("\nTeste de conexão concluído com sucesso!")
            print("O banco está pronto para uso!")
            return True
            
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        print("\nPossíveis soluções:")
        print("1. Verifique se o PostgreSQL está rodando")
        print("2. Confirme as credenciais no arquivo .env")
        print("3. Certifique-se de que o banco de dados existe")
        print("4. Execute: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
