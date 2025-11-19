import os
import sys
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    print("Inicializando banco de dados do IFinance...")
    print("=" * 50)
    
    try:
        from app import create_app
        from app.models import db, User, TypeOperation, EntrySAC
        
        print("Importações realizadas com sucesso")
        
        app = create_app()
        
        with app.app_context():
            print("\nVerificando estado atual do banco...")
            
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            expected_tables = ['users', 'type_operations', 'entry_sac']
            existing_expected = [table for table in expected_tables if table in existing_tables]
            
            if existing_expected:
                print(f"As seguintes tabelas já existem: {existing_expected}")
                response = input("Deseja recriar todas as tabelas? Isso apagará todos os dados! (s/N): ")
                
                if response.lower() != 's':
                    print("Operação cancelada pelo usuário.")
                    return False
                
                print("Removendo tabelas existentes...")
                db.drop_all()
                print("Tabelas removidas!")
            
            print("\nCriando tabelas...")
            db.create_all()
            print("Tabelas criadas com sucesso!")
            
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tabelas disponíveis: {tables}")
            
            print("\nVerificando dados iniciais...")
            
            if TypeOperation.query.count() == 0:
                print("Criando tipos de operação padrão...")
                
                default_types = [
                    {
                        'name': 'Sistema de Amortização Constante (SAC)',
                        'description': 'Sistema de Amortização Constante (SAC) consiste em parcelas de valor variado que decrescem de forma constante.'
                    }
                ]
                
                for type_data in default_types:
                    type_op = TypeOperation(**type_data)
                    db.session.add(type_op)
                
                db.session.commit()
                print(f"{len(default_types)} tipos de operação criados!")
            else:
                print("Tipos de operação já existem no banco")
            
            print("\nEstado final do banco:")
            print(f"Usuários: {User.query.count()}")
            print(f"Tipos de operação: {TypeOperation.query.count()}")
            print(f"Operações SAC: {EntrySAC.query.count()}")
            
            print("\nInicialização do banco concluída com sucesso!")
            print("A aplicação está pronta para uso!")
            
    except Exception as e:
        print(f"Erro durante a inicialização: {e}")
        print("\nPossíveis soluções:")
        print("1. Verifique se o PostgreSQL está rodando")
        print("2. Confirme as credenciais no arquivo .env")
        print("3. Certifique-se de que o banco de dados existe")
        print("4. Execute: pip install -r requirements.txt")
        return False
    
    return True

def reset_database():
    print("ATENÇÃO: Esta operação irá remover TODOS os dados do banco!")
    print("=" * 60)
    
    response = input("Tem certeza que deseja continuar? Digite 'CONFIRMO' para prosseguir: ")
    
    if response != 'CONFIRMO':
        print("Operação cancelada.")
        return False
    
    try:
        from app import create_app
        from app.models import db
        
        app = create_app()
        
        with app.app_context():
            print("Removendo todas as tabelas...")
            db.drop_all()
            print("Todas as tabelas foram removidas!")
            
            print("Recriando tabelas...")
            db.create_all()
            print("Tabelas recriadas com sucesso!")
            
    except Exception as e:
        print(f"Erro durante o reset: {e}")
        return False
    
    print("Reset do banco concluído!")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Script de inicialização do banco de dados')
    parser.add_argument('--reset', action='store_true', 
                       help='Remove todas as tabelas e dados')
    
    args = parser.parse_args()
    
    if args.reset:
        success = reset_database()
    else:
        success = init_database()
    
    sys.exit(0 if success else 1)
