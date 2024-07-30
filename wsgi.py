import sys
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app as portal_app

# Add the paths to the projects
sys.path.insert(0, '/home/yourusername/WartemProjectHub/projects/existing_project')
sys.path.insert(0, '/home/yourusername/WartemProjectHub/projects/new_project')

# Import the project apps
from existing_project.app import app as existing_app
from new_project.app import app as new_app

# Create the DispatcherMiddleware to route to different projects
application = DispatcherMiddleware(portal_app, {
    '/existing-project': existing_app,
    '/new-project': new_app
})
