![Python](https://img.shields.io/badge/language-Python-blue.svg)
![HTML](https://img.shields.io/badge/language-HTML-orange.svg)
![CSS](https://img.shields.io/badge/language-CSS-green.svg)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![Jinja](https://img.shields.io/badge/template%20engine-Jinja-yellow.svg)

# WartemProjectHub

## Overview
WartemProjectHub is a centralized platform for managing and showcasing various projects developed under the name Wartem. This hub provides a unified interface for accessing multiple projects, each with its own unique functionality and purpose.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Project Hub](#running-the-project-hub)
  - [Creating a New Project](#creating-a-new-project)
- [Project List](#project-list)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Features
- Centralized management of multiple projects
- Dynamic project discovery and integration
- Easy-to-use interface for navigating between projects
- Customizable project display names
- Automated project creation tool

## Project Structure
```
WartemProjectHub/
├── app.py # Main application file
├── wsgi.py # WSGI entry point
├── requirements.txt # Main project dependencies
├── create_project.py # Script for creating new projects
├── templates/ # HTML templates for the main app
│ ├── base.html
│ └── home.html
├── static/ # Static files (CSS, JS, images)
├── projects/ # Directory containing all projects
│ ├── existing_project/
│ │ ├── app.py
│ │ ├── routes.py
│ │ ├── requirements.txt
│ │ ├── project_config.json
│ │ └── templates/
│ └── new_project/
│ ├── ...
└── project_template/ # Template for new projects
├── app.py
├── routes.py
└── templates/
└── project.html
```

## Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation
1. Clone the repository:
https://github.com/wartem/WartemProjectHub

2. Navigate to the project directory: cd WartemProjectHub
3. Install the required dependencies: pip install -r requirements.txt

## Usage

### Running the Project Hub
1. Start the application: python app.py
2. Open a web browser and navigate to `http://localhost:5000`

### Creating a New Project
1. Run the project creation script: python create_project.py

2. Follow the prompts to name your project and set up initial configurations.

## Project List
- A version of [CO2-Transport-Calculator-Example](https://github.com/Wartem/CO2-Transport-Calculator-Example)

## Acknowledgements
This project was developed with the significant assistance of Perplexity AI (https://www.perplexity.ai), an innovative AI tool that greatly facilitated the research and development process. Perplexity AI provided invaluable guidance on project structure, coding practices, and documentation. It helped streamline the gathering of information and offered crucial insights into the structure and functionality of the application.

The AI's contributions were instrumental in clarifying concepts, generating code, and creating comprehensive documentation for this project. This acknowledgment serves to recognize the pivotal role that Perplexity AI played in the development of WartemProjectHub.

## License
This project is licensed under the MIT License.
