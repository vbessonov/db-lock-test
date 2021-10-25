# db-lock-test
Test Python app showing how database deadlocks happen in multithreaded applications and how to resolve them.

# Usage
1. Clone the repository:
```bash
git clone https://github.com/vbessonov/db-lock-test.git
cd db-lock-test
```

2. Create a virtual environment using pyenv:
```bash
pyenv virtualenv 3.9.7 db-lock-test
pyenv activate db-lock-test
```

2. Install required dependencies:
```bash
(venv) -> pip install -U pip
(venv) -> pip install -r requrements.txt 
```

3. Set the environment variables:
```bash
(venv) -> export DB_USER=<local database user name>
(venv) -> export DB_NAME=<database name>  # the database must exist
```

4. Run the app in the deadlock mode:
```bash
(venv) -> python main.py 1
```

5. Look at the deadlock error in the log:
```
sqlalchemy.exc.OperationalError: (psycopg2.errors.DeadlockDetected) deadlock detected
DETAIL:  Process 46371 waits for ShareLock on transaction 208287; blocked by process 46370.
Process 46370 waits for ShareLock on transaction 208288; blocked by process 46371.
HINT:  See server log for query details.
CONTEXT:  while updating tuple (0,6) in relation "workcoveragerecords"

[SQL: UPDATE workcoveragerecords SET timestamp = '2021-10-25 17:23:41.129207' WHERE id = 5]
(Background on this error at: https://sqlalche.me/e/14/e3q8)
```

6. Run the app in the no-deadlock mode and ensure that there are no errors in the log:
```bash
(venv) -> python main.py 2
```