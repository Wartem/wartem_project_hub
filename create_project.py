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
    template_dir = os.path.join(script_dir, 'project_template')
    projects_dir = os.path.join(script_dir, 'projects')
    new_project_dir = os.path.join(projects_dir, project_name)

    # Check if project already exists
    if os.path.exists(new_project_dir):
        print(f"Error: Project '{project_name}' already exists.")
        return

    # Check if template directory exists
    if not os.path.exists(template_dir):
        print(f"Error: Template directory '{template_dir}' does not exist.")
        return

    try:
        # Create projects directory if it doesn't exist
        os.makedirs(projects_dir, exist_ok=True)

        # Copy template to new project directory
        shutil.copytree(template_dir, new_project_dir)

        # Rename project.html to project_name.html
        os.rename(
            os.path.join(new_project_dir, 'templates', 'project.html'),
            os.path.join(new_project_dir, 'templates', f'{project_name}.html')
        )

        # Update project.html content
        html_path = os.path.join(new_project_dir, 'templates', f'{project_name}.html')
        with open(html_path, 'r') as file:
            content = file.read()
        
        content = content.replace('{{ project_name }}', display_name)
        
        with open(html_path, 'w') as file:
            file.write(content)

        # Update routes.py
        routes_path = os.path.join(new_project_dir, 'routes.py')
        with open(routes_path, 'r') as file:
            content = file.read()
        
        content = content.replace("'project'", f"'{project_name}'")
        content = content.replace("'project.html'", f"'{project_name}.html'")
        
        with open(routes_path, 'w') as file:
            file.write(content)

        # Create project_config.json
        config_path = os.path.join(new_project_dir, 'project_config.json')
        config_data = {
            "display_name": display_name
        }
        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

        # Create requirements.txt
        requirements_path = os.path.join(new_project_dir, 'requirements.txt')
        requirements_content = """"""
        with open(requirements_path, 'w') as requirements_file:
            requirements_file.write(requirements_content)

        print(f"Project '{project_name}' created successfully with display name '{display_name}'.")
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")

if __name__ == "__main__":
    create_project()
