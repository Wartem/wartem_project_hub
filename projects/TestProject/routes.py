import os
from flask import Blueprint, render_template

project_name = os.path.basename(os.path.dirname(__file__))
bp = Blueprint(project_name, __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template(f'{project_name}.html')