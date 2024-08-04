import os
import shutil
import json

def create_project():
    # Get the project name from the user
    project_name = input("Enter the name of the new project (alphanumeric only): ").strip()

    # Validate project name
    if not project_name or not project_name.isalnum():
        print("Invalid project name. Please use alphanumeric characters only.")
        return

    # Get the display name from the user
    display_name = input("Enter the display name for the project (press Enter to use the project name): ").strip()
    if not display_name:
        display_name = project_name

    # Get the directory of the script being executed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    template_dir = os.path.join(script_dir, 'project_templates')
    projects_dir = os.path.join(script_dir, 'projects')
    new_project_dir = os.path.join(projects_dir, project_name)

    # Check if project already exists
    if os.path.exists(new_project_dir):
        print(f"Error: Project '{project_name}' already exists.")
        return

    try:
        # Create projects directory if it doesn't exist
        os.makedirs(projects_dir, exist_ok=True)

        # Copy template to new project directory
        shutil.copytree(template_dir, new_project_dir)

        # Update project_config.json
        config_path = os.path.join(new_project_dir, 'project_config.json')
        config_data = {
            "display_name": display_name
        }
        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

        # Update routes.py with the correct project name
        routes_path = os.path.join(new_project_dir, 'routes.py')
        with open(routes_path, 'r') as file:
            content = file.read()
        content = content.replace('PROJECT_NAME', project_name)
        with open(routes_path, 'w') as file:
            file.write(content)

        print(f"Project '{project_name}' created successfully with display name '{display_name}'.")
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")

if __name__ == "__main__":
    create_project()