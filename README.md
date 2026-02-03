# IFinance - Sistema de Simuladores Financeiros 
 
Sistema Flask completo com simuladores financeiros para SAC, PRICE, Crédito, Lucro e CET. Interface web moderna com autenticação de usuários.

## ✨ Funcionalidades

- 🏠 **Página Inicial**: Landing page moderna e responsiva
- 🔐 **Autenticação**: Sistema completo de login e cadastro
- 📊 **Simuladores**: SAC, PRICE, Crédito, Lucro e CET
- 📋 **Histórico**: Visualização e gerenciamento de simulações
- 🎨 **Interface**: Design moderno e responsivo
- 💾 **Banco de Dados**: PostgreSQL com SQLAlchemy

## 🚀 Configuração Rápida

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados

#### Criar banco PostgreSQL:
```sql
CREATE DATABASE finance_db;
```

#### Configurar variáveis de ambiente:
Copie o arquivo `.env.example` para `.env` e ajuste as configurações:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finance_db
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
SECRET_KEY=sua-chave-secreta
FLASK_DEBUG=True
FLASK_ENV=development
```

### 3. Inicializar Banco de Dados
```bash
python init_db.py
```

### 4. Executar Aplicação
```bash
python wsgi.py
```

Acesse: http://localhost:5000

## 🎯 Páginas Disponíveis

### Interface Web Pública
- `/` - Página inicial com apresentação do sistema
- `/login` - Página de login
- `/register` - Página de cadastro

### Interface Web Autenticada (Requer Login)
- `/dashboard` - Dashboard principal com simuladores
- `/simulate` - Simuladores financeiros (SAC, PRICE, Crédito, Lucro, CET)
- `/history` - Histórico de simulações do usuário
- `/profile` - Perfil e configurações do usuário
- `/logout` - Logout do usuário

### API Endpoints
- `GET /api/operations` - Listar operações
- `GET /api/operations/<id>` - Buscar operação por ID
- `POST /api/operations` - Criar nova operação
- `DELETE /api/operations/<id>` - Deletar operação
- `GET /api/health` - Status da aplicação

## 📊 Estrutura do Banco

O sistema criará automaticamente as seguintes tabelas:

- **users**: Usuários do sistema (nome, email, senha, telefone)
- **type_operations**: Tipos de operação financeira
- **entry_sac**: Operações SAC com cálculos e resultados

## 🎨 Templates Implementados

### Templates Base
- `base.html` - Template base com layout responsivo
- `base_authenticated.html` - Template base para usuários logados (com sidebar)
- `index.html` - Página inicial moderna
- `sidebar.html` - Componente de sidebar para navegação

### Templates Públicos
- `auth/login.html` - Formulário de login
- `auth/register.html` - Formulário de cadastro

### Templates Autenticados
- `dashboard.html` - Dashboard principal com simuladores
- `simular.html` - Interface de simuladores com tabs
- `history/history.html` - Histórico com filtros e tabela
- `simulation_detail.html` - Detalhes de simulação
- `profile.html` - Perfil e configurações do usuário

### Templates de Erro
- `exceptions/401.html` - Não autorizado
- `exceptions/403.html` - Acesso proibido
- `exceptions/404.html` - Página não encontrada
- `exceptions/500.html` - Erro interno do servidor

## 🎨 CSS e Estilização

### Arquivos CSS
- `global.css` - Estilos globais, utilitários e mensagens flash
- `login.css` - Estilos específicos para autenticação
- `simulate.css` - Estilos para simuladores e sidebar

### Características do Design
- ✅ Design responsivo (mobile-first)
- ✅ Paleta de cores consistente (verde #006400)
- ✅ Tipografia Roboto do Google Fonts
- ✅ Animações suaves e transições
- ✅ Mensagens flash com auto-dismiss
- ✅ Tabelas responsivas com hover effects

## 🛠️ Estrutura do Projeto

```
IFinance/
├── app/
│   ├── controllers/          # Controladores (rotas)
│   │   ├── auth_controller.py    # Autenticação
│   │   ├── main_controller.py    # Páginas principais
│   │   ├── user_controller.py    # Gestão de usuários
│   │   └── type_operation_controller.py
│   ├── models/               # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── entry_sac.py
│   │   └── type_operation.py
│   ├── templates/            # Templates Jinja2
│   │   ├── auth/
│   │   ├── history/
│   │   ├── exceptions/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── simular.html
│   │   └── simulation_detail.html
│   ├── config.py             # Configurações Flask
│   ├── routes.py             # Rotas da API
│   └── __init__.py
├── static/                   # Arquivos estáticos
│   ├── css/                  # Estilos CSS
│   ├── img/                  # Imagens
│   └── js/                   # JavaScript
├── instance/                 # Banco de dados
├── wsgi.py                   # Aplicação Flask
├── init_db.py               # Inicialização do banco
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🔧 Funcionalidades Implementadas

### ✅ Concluído
- [x] Estrutura base do Flask com blueprints
- [x] Modelos SQLAlchemy para usuários e operações
- [x] Sistema de autenticação completo com sessões
- [x] Área restrita para usuários logados
- [x] Sidebar de navegação para usuários autenticados
- [x] Dashboard principal com simuladores
- [x] Página de perfil com configurações
- [x] Templates responsivos com Jinja2
- [x] CSS moderno e responsivo
- [x] Mensagens flash para feedback
- [x] Interface de simuladores com tabs
- [x] Página de histórico com filtros
- [x] Páginas de erro personalizadas
- [x] API REST para operações

### 🚧 Em Desenvolvimento
- [ ] Cálculos financeiros (SAC, PRICE, etc.)
- [ ] Geração de relatórios em PDF
- [ ] Gráficos e visualizações
- [ ] Sistema de permissões
- [ ] Testes automatizados

## 🎯 Próximos Passos

1. **Implementar cálculos financeiros** nos controllers
2. **Adicionar validações** mais robustas
3. **Criar testes automatizados** para todas as funcionalidades
4. **Implementar hash de senhas** com bcrypt
5. **Adicionar sistema de recuperação** de senha
6. **Criar dashboard** com estatísticas
7. **Implementar exportação** para Excel/PDF

## 📝 Notas de Desenvolvimento

- Os templates usam Jinja2 com herança de templates
- O CSS é modular e responsivo
- As mensagens flash são exibidas automaticamente
- O sistema de autenticação usa sessões Flask
- Todos os formulários têm validação básica
- A interface é totalmente responsiva

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste todas as funcionalidades
5. Faça um pull request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
