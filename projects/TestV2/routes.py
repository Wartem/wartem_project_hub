import os
import json
from flask import Blueprint, render_template, request
from .project_main import start

project_dir = os.path.dirname(__file__)
project_name = os.path.basename(project_dir)

# Read display_name from project_config.json
config_path = os.path.join(project_dir, 'project_config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    display_name = config.get('display_name', project_name)

bp = Blueprint(project_name, __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('index.html', project_name=project_name, display_name=display_name)

@bp.route('/project')
def start_project():
    result = start()
    result['project_name'] = project_name
    result['display_name'] = display_name
    return render_template('project.html', **result)