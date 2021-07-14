# How to install
To install dependencies for development use: `$ pip install -r requirements-dev.txt`

# How to run
## For development
To run it in local `$ uvicorn app:app --reload`

# How to use
Swagger page: `http://127.0.0.1:8000/docs`
Request example: `$ curl GET 'http://127.0.0.1:8000/api/v1/score/django/django'`

# Run in Docker
Create image: `$ docker build -t <name> .`
Run container: `$docker run --rm -p 8000:8000 juancamiloceron/github`


# How to test
## Static code
- To check PEP8: `$ flake8`

## Unit tests
- This will run unittest and functional: `$ pytest`
- Coverage report: `$ pytest --cov=. tests/`

## Integration test
Be aware this is going to actually hit github. This may fail due the restrictions of **0.5s** latency
- This will run only integration tests: `$ pytest tests/tests_integration/`


# TODO
- [ ] Use classes for tests and use fixtures
- [ ] Add logs