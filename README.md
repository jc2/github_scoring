# How to install
To install dependencies for development use: `$ pip install -r requirements-dev.txt`

# How to run
## For development
To run it in local `$ uvicorn app:app --reload`

# How to use
Swagger page: `http://127.0.0.1:8000/docs`

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