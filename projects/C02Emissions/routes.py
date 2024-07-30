from flask import Blueprint
from .input_app import handle_input
from .result_app import show_result as show_result_function

bp = Blueprint('C02Emissions', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    return handle_input()

@bp.route('/result/<distance>')
def show_result(distance):
    return show_result_function(distance)