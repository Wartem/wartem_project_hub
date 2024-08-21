import os
import json
import contextlib
from flask import Blueprint, render_template, redirect, url_for, current_app, g

@contextlib.contextmanager
def temporary_sys_path(path):
    import sys
    original_sys_path = sys.path.copy()
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path = original_sys_path

project_dir = os.path.dirname(__file__)
project_name = os.path.basename(project_dir)

# Read display_name from project_config.json
config_path = os.path.join(project_dir, 'project_config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    display_name = config.get('display_name', project_name)

bp = Blueprint(project_name, __name__, template_folder='templates')

@bp.before_request
def before_request():
    g.project_name = project_name
    g.display_name = display_name

@bp.route('/')
def index():
    # Check if we're running as an individual project
    if current_app.name == g.project_name:
        # If running individually, redirect to the project page
        return redirect(url_for(f'{g.project_name}.start_project'))
    # If running as part of main_app, show the index page
    return render_template('index.html', project_name=g.project_name, display_name=g.display_name)

@bp.route('/project')
def start_project():
    with temporary_sys_path(project_dir):
        from .project_main import start
    
    result = start()
    result['project_name'] = g.project_name
    result['display_name'] = g.display_name
    return render_template('project.html', **result)