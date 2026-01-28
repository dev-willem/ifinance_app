from flask import Blueprint, request
from .models import db
from .controllers import auth_controller, calculator_controller, main_controller, type_operation_controller, user_controller

# Blueprint para páginas principais
main_bp = Blueprint('main', __name__)

# Blueprint para autenticação (prefixo /auth)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Blueprint para API (usuarios / tipos)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ---------------------- AUTH ------------------------

@auth_bp.route('/login', methods=['GET'])
def login():
    return auth_controller.login()

@auth_bp.route('/register', methods=['GET'])
def register():
    return auth_controller.register()

@auth_bp.route('/login', methods=['POST'])
def login_user():
    return auth_controller.login_user()

@auth_bp.route('/register', methods=['POST'])
def register_user():
    return auth_controller.register_user()

# Permitir GET aqui por compatibilidade com links, aceitar POST se preferir
@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout_user():
    return auth_controller.logout_user()

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    return auth_controller.get_current_user()

# ---------------------- USERS (API) -----------------------

@api_bp.route('/users', methods=['GET'])
def get_all_users():
    return user_controller.get_all_users()

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return user_controller.get_user_by_id(user_id)

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return user_controller.update_user(user_id)

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user_controller.delete_user(user_id)

# ---------------------- TYPES (API) -----------------------

@api_bp.route('/types', methods=['GET'])
def get_all_types():
    return type_operation_controller.get_all_types()

@api_bp.route('/types/<int:type_id>', methods=['GET'])
def get_type_by_id(type_id):
    return type_operation_controller.get_type_by_id(type_id)

@api_bp.route('/types/<int:type_id>/operations', methods=['GET'])
def get_operations_by_type(type_id):
    return type_operation_controller.get_operations_by_type(type_id)

@api_bp.route('/types', methods=['POST'])
def create_type():
    return type_operation_controller.create_type()

# -------------------- MAIN PAGES ---------------------

@main_bp.route('/', methods=['GET'])
def index():
    return main_controller.index()

@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return main_controller.dashboard()

@main_bp.route('/simulate', methods=['GET'])
def simulate():
    return main_controller.simulate()

@main_bp.route('/history', methods=['GET'])
def history():
    return main_controller.history()

@main_bp.route('/profile', methods=['GET'])
def profile():
    return main_controller.profile()

# Compatibilidade: expor `/login`, `/register` e `/logout` sob o blueprint `main`
# para preservar referências existentes em templates que usam `main.login` / `main.register`.
@main_bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login_compat():
    if request.method == 'POST':
        return auth_controller.login_user()
    return auth_controller.login()

@main_bp.route('/register', methods=['GET', 'POST'], endpoint='register')
def register_compat():
    if request.method == 'POST':
        return auth_controller.register_user()
    return auth_controller.register()

@main_bp.route('/logout', methods=['GET', 'POST'], endpoint='logout_user')
def logout_user():
    return auth_controller.logout_user()

# -------------------- SIMULATIONS --------------------

@main_bp.route('/simulate/sac', methods=['POST'])
def simulate_sac():
    return main_controller.simulate_sac()

@main_bp.route('/simulate/price', methods=['POST'])
def simulate_price():
    return main_controller.simulate_price()

@main_bp.route('/simulate/credit', methods=['POST'])
def simulate_credit():
    return main_controller.simulate_credit()

@main_bp.route('/simulate/profit', methods=['POST'])
def simulate_profit():
    return main_controller.simulate_profit()

@main_bp.route('/simulate/cet', methods=['POST'])
def simulate_cet():
    return main_controller.simulate_cet()

@main_bp.route('/simulation/<int:type_id>/<int:simulation_id>', methods=['GET'])
def view_simulation(type_id, simulation_id):
    return main_controller.view_simulation(type_id, simulation_id)

@main_bp.route('/simulation/<int:simulation_id>/destroy', methods=['POST'])
def destroy_simulation(simulation_id):
    return main_controller.destroy_simulation(simulation_id)

# ---------------------- PROFILES ------------------

@main_bp.route('/update_profile', methods=['POST'])
def update_profile():
    return main_controller.update_profile()

@main_bp.route('/change_password', methods=['POST'])
def change_password():
    return main_controller.change_password()

@main_bp.route('/update_settings', methods=['POST'])
def update_settings():
    return main_controller.update_settings()

# ---------------------- CALCULATORS ------------------

@main_bp.route('/calculator/sac', methods=['POST'])
def sac_system_calculation():
    return calculator_controller.sac_system_api()

# ------------------ BLUEPRINT REGISTER ----------------

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
