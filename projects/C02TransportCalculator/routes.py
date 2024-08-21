from flask import Blueprint
from .input_app import handle_input
from .result_app import show_result as show_result_function

import sys
#print(f"Python path in routes.py: {sys.path}")
try:
    import pandas as pd
    print("Pandas imported successfully")
except ImportError as e:
    print(f"Failed to import pandas: {e}")
    print(f"Pandas location: {pd.__file__}" if 'pd' in locals() else "Pandas not found")

bp = Blueprint('CO2TransportCalculator', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    return handle_input()

@bp.route('/result/<distance>')
def show_result(distance):
    return show_result_function(distance)

@bp.route('/test')
def test():
    return "C02TransportCalculator test route is working!"