# drf-react-social

Social network for posting, based on DRF and React.

[![Build Status](https://travis-ci.org/Hephest/drf-react-social.svg?branch=master)](https://travis-ci.org/Hephest/drf-react-social)
![GitHub last commit](https://img.shields.io/github/last-commit/Hephest/drf-react-social)
[![Updates](https://pyup.io/repos/github/Hephest/drf-react-social/shield.svg)](https://pyup.io/repos/github/Hephest/drf-react-social/)
[![Python 3](https://pyup.io/repos/github/Hephest/drf-react-social/python-3-shield.svg)](https://pyup.io/repos/github/Hephest/drf-react-social/)

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
    - [Development](#development)
- [To Do](#to-do)

## Features

- Django 3.0+
- Django REST Framework 3.11+
- PostgreSQL 12.3+
- Fully dockerized, local development via docker-compose
- CLI automation bot for testing purposes ([see here](bot/README.md))

## Getting Started

### Prerequisites

Project based on Docker containers. As basic prerequisites, you need to get:

- **Docker v.19.03.11-ce** (Linux) or **Docker Machine** (Windows, MacOS)
- **Docker Compose v.1.26.0**

### Installing

Clone repository to your local machine:

    git clone https://github.com/Hephest/drf-react-social.git
    
Create and fill `.env` file (example below):

```.env
# Django
DJANGO_SECRET_KEY = 'h*3-=2ts1zznjts4rl+4ehakk7p3ncdh-jevt3y03h9ze(+3a7'

# PostgreSQL
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'db'
DB_PORT = 5432
```

Run `docker-compose`:

    docker-compose up

### Development

1. Set up virtual environment via provided `requirements.txt` in `backend` directory:
    
        python -m venv venv/
        source venv/bin/activate
        pip install -r backend/requirements.txt

2. Write some code and tests
3. Run tests via `docker-compose`:

        docker-compose run web python backend/manage.py test blog.tests

## To do

### Project
- [x] ~~Documentation~~
- [ ] `Docker` and `docker-compose` setup
    - [x] ~~backend container~~
    - [ ] `frontend` container
    - [x] ~~.env fle support~~

### Backend
- [x] ~~Nose test runner~~
- [x] ~~Coverage report~~
- [x] ~~isort and flake8 support~~
- [x] ~~Testcases for all API parts~~
    - [x] ~~User sign up~~
    - [x] ~~JWT tokens~~
    - [x] ~~Posts & likes~~
- [x] ~~PostgreSQL~~

### Frontend
- [ ] `React` project folder
- [ ] Components
- [ ] Connect to API (`axios`)