# drf-react-social

Social network for posting, based on DRF and React.

## Testing

Project support `Nose` test runner (`django-nose`) and coverage reports (`coverage`).

Running tests:

    python manage.py test
    
Example report:

    nosetests --cover-erase --cover-package=blog --verbosity=1
    Creating test database for alias 'default'...
    ...........
    ----------------------------------------------------------------------
    Ran 11 tests in 2.455s
    
    OK
    Destroying test database for alias 'default'...
    Name                              Stmts   Miss  Cover   Missing
    ---------------------------------------------------------------
    blog/__init__.py                      0      0   100%
    blog/admin.py                         1      0   100%
    blog/apps.py                          3      3     0%   1-5
    blog/migrations/0001_initial.py       7      0   100%
    blog/migrations/__init__.py           0      0   100%
    blog/mixins.py                       21     10    52%   11-13, 17-19, 23-26
    blog/models.py                       21      1    95%   23
    blog/serializers.py                  30      0   100%
    blog/tests.py                        89      0   100%
    blog/urls.py                          8      0   100%
    blog/utils.py                        20     10    50%   10-12, 16-17, 23-25, 29-30
    blog/views.py                        25      1    96%   19
    ---------------------------------------------------------------
    TOTAL                               225     25    89%


## To do

### Project
- [ ] Documentation
- [ ] `Docker` and `docker-compose` setup
    - [ ] `backend` container
    - [ ] `frontend` container
    - [ ] `.env` fle support

### Backend
- [x] ~~Nose test runner~~
- [x] ~~Coverage report~~
- [ ] Testcases for all API parts
    - [x] ~~User sign up~~
    - [x] ~~JWT tokens~~
    - [ ] Posts & likes
- [ ] `PostgreSQL`

### Frontend
- [ ] `React` project folder
- [ ] Components
- [ ] Connect to API (`axios`)