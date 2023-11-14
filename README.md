# Algebra API

## Overview
Algebra API is a Django-based web application designed to evaluate algebraic expressions. It features a RESTful API that allows users to input algebraic expressions, see the results, and view a history of operations.

## Features
- Evaluate algebraic expressions.
- View a history of evaluated expressions.
- RESTful API endpoints for interaction.

## Prerequisites
- Python 3.11.5
- Django==4.2.7
- Docker
- Docker Compose
## Project's structure

```text
├── algebra_engine ·················· Django app
│  ├── migrations ··················· Database migration files
│  ├── tests ························ Test cases for the application
│  ├──── constance.py ··············· Constance where keep expressions for test
│  ├──── test_models.py ············· Test cases for models
│  └──── test_views.py ·············· Test cases for views
│  ├── admin.py ····················· Django admin configuration
│  ├── apps.py ······················ App configuration
│  ├── expression_validator.py ······ Validator for algebraic expressions
│  ├── models.py ···················· Database models
│  ├── parser.py ···················· Parser for processing expressions
│  ├── serializers.py ··············· Serializers for converting data to/from JSON
│  ├── urls.py ······················ URL declarations for the app
│  └── views.py ····················· Views for handling requests and responses
├── AlgebraAPI ······················ Main project directory
│  ├── asgi.py ······················ ASGI config for deployment
│  ├── settings.py ·················· Django project settings
│  ├── urls.py ······················ Main URL declarations for the project
│  └── wsgi.py ······················ WSGI config for deployment
├── templates ······················· Templates directory for HTML templates
│  └── index.html ··················· Main HTML template
├── .env.example ···················· Example environment variables file 
├── .gitignore ······················ Specifies intentionally untracked files to ignore
├── docker-compose.yml ·············· Docker Compose configuration
├── Dockerfile ······················ Dockerfile for building the Docker image
├── error_messages.py ··············· Error messages for django apps
├── manage.py ······················· Command-line utility for administrative tasks
├── messages.py ····················· Custom messages or constants
├── README.md ······················· README file with project details (you're here)
└── requirements.txt ················ Python dependencies file
```
## Installation

### Clone the Repository
```bash
git clone git@github.com:Arno-Gevorgyan/Home-Assignment-Test-task.git
cd AlgebraAPI
```

### Python (via `venv`)

Make sure you have python's venv module available. Then initialize the new venv:
```bash
python3 -m venv venv
```

Then, declare the newly created environment:
```bash
source venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

#### Create `.env` file (you can base in on `.env.example`)

You may now export the local environment variables following way (specify path to the env-file):
```
export $(grep -v '^#' .env | xargs)
```

Regular Django manager commands are then available:
```
python3 manage.py migrate
python manage.py createsuperuser
python3 manage.py runserver
```

## Dockerization
```
docker-compose up --build -d 
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```