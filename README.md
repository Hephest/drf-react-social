# drf-react-social

Social network for posting, based on DRF and React.

[![Build Status](https://travis-ci.org/Hephest/drf-react-social.svg?branch=master)](https://travis-ci.org/Hephest/drf-react-social)
![GitHub last commit](https://img.shields.io/github/last-commit/Hephest/drf-react-social)

## Testing

Project support `Nose` test runner (`django-nose`) and coverage reports (`coverage`).

Running tests:

    python manage.py test
    
Example report:

    nosetests --cover-erase --cover-package=blog --verbosity=1
    Creating test database for alias 'default'...
    ......................
    ----------------------------------------------------------------------
    Ran 22 tests in 7.905s
    
    OK
    Destroying test database for alias 'default'...
    Name                              Stmts   Miss  Cover   Missing
    ---------------------------------------------------------------
    blog/__init__.py                      0      0   100%
    blog/admin.py                         1      0   100%
    blog/apps.py                          3      3     0%   1-5
    blog/migrations/0001_initial.py       7      0   100%
    blog/migrations/__init__.py           0      0   100%
    blog/mixins.py                       21      0   100%
    blog/models.py                       22      1    95%   26
    blog/serializers.py                  30      0   100%
    blog/tests.py                       182      0   100%
    blog/urls.py                          8      0   100%
    blog/utils.py                        20      0   100%
    blog/views.py                        25      0   100%
    ---------------------------------------------------------------
    TOTAL                               319      4    99%

## To do

### Project
- [ ] Documentation
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