# task-manager
A REST API which allows tasks to be moved between different status'.
Users can only see their own tasks, and tasks can only have one of 4 different status at any given time: 'Pending', 'Doing', 'Blocked', 'Done'.
Delete tasks are removed from a users list, but they are be moved to a history table for audit purposes.

There is support for both python 3.9 and 3.10, all code is formatted using Black formatting.
Makes use of FastAPI framework
