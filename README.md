# task-manager
A REST API which allows tasks to be moved between different status'.
Users can only see their own tasks, and tasks can only have one of 4 different status at any given time: 'Pending', 'Doing', 'Blocked', 'Done'.
Delete tasks are removed from a users list, but they are be moved to a history table for audit purposes.

There is support for both python 3.9 and 3.10, all code is formatted using Black formatting.
Makes use of FastAPI framework


Docs are provided by swagger http://127.0.0.1:8000/docs

Getting Started:

pull this repo and cd in to the folder.
make sure you're in a virtual env with python 3.9+ in use

run `curl -sSL https://install.python-poetry.org | python3 -` to install poetry

run `poetry install`

To run server:
`uvicorn main:app --reload`
running this will automatically run alembic migrations to set up db with some test data.

To check formatting run `black ./pathtofile`