from flask import Blueprint, request, jsonify
from .models import db, EntrySAC, User, TypeOperation
from .controllers import *

routes_bp = Blueprint('main', __name__)

# ---------------------- AUTH ------------------------

@routes_bp.route('/auth/login')
def login():
    return auth_controller.login()

@routes_bp.route('/auth/register')
def register():
    return auth_controller.register()

@routes_bp.route('/auth/login', methods=['POST'])
def login_user():
    return auth_controller.login_user()

@routes_bp.route('/auth/register', methods=['POST'])
def register_user():
    return auth_controller.register_user()

@routes_bp.route('/auth/logout')
def logout_user():
    return auth_controller.logout_user()

# ---------------------- USERS -----------------------

@routes_bp.route('/users', methods=['GET'])
def get_all_users():
    return user_controller.get_all_users()

@routes_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return user_controller.get_user_by_id(user_id)

@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return user_controller.update_user(user_id)

@routes_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user_controller.delete_user(user_id)

# ---------------------- TYPES -----------------------

@routes_bp.route('/types', methods=['GET'])
def get_all_types():
    return type_operation_controller.get_all_types()

@routes_bp.route('/types/<int:type_id>', methods=['GET'])
def get_type_by_id(type_id):
    return type_operation_controller.get_type_by_id(type_id)

@routes_bp.route('/types/<int:type_id>/operations', methods=['GET'])
def get_operations_by_type(type_id):
    return type_operation_controller.get_operations_by_type(type_id)

@routes_bp.route('/types', methods=['POST'])
def create_type():
    return type_operation_controller.create_type()

# -------------------- MAIN PAGES ---------------------

@routes_bp.route('/')
def index():
    return main_controller.index()

@routes_bp.route('/dashboard')
def dashboard():
    return main_controller.dashboard()

@routes_bp.route('/simulate')
def simulate():
    return main_controller.simulate()

@routes_bp.route('/history')
def history():
    return main_controller.history()

@routes_bp.route('/profile')
def profile():
    return main_controller.profile()

# -------------------- SIMULATIONS --------------------

@routes_bp.route('/simulate/sac', methods=['POST'])
def simulate_sac():
    return main_controller.simulate_sac()

@routes_bp.route('/simulate/price', methods=['POST'])
def simulate_price():
    return main_controller.simulate_price()

@routes_bp.route('/simulate/credit', methods=['POST'])
def simulate_credit():
    return main_controller.simulate_credit()

@routes_bp.route('/simulate/profit', methods=['POST'])
def simulate_profit():
    return main_controller.simulate_profit()

@routes_bp.route('/simulate/cet', methods=['POST'])
def simulate_cet():
    return main_controller.simulate_cet()

@routes_bp.route('/simulation/<int:simulation_id>')
def view_simulation(simulation_id):
    return main_controller.view_simulation(simulation_id)

@routes_bp.route('/update_profile', methods=['POST'])
def update_profile():
    return main_controller.update_profile()

@routes_bp.route('/change_password', methods=['POST'])
def change_password():
    return main_controller.change_password()

@routes_bp.route('/update_settings', methods=['POST'])
def update_settings():
    return main_controller.update_settings()

# ---------------------- CALCULATORS ------------------

@routes_bp.route('/calculator/sac', methods=['POST'])
def sac_system_calculation():
    return calculator_controller.sac_system_calculation()

# ------------------ BLUEPRINT REGISTER ----------------

def register_routes(app):
    app.register_blueprint(routes_bp)
