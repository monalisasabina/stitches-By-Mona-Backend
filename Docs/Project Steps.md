# Project steps

1. To install dependancies and enter virtual environment

```bash
pipenv install
pipenv shell
```

2. Configure ```FLASK_APP``` and ```FLASK_RUN_PORT```

```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```

4. Installed serializerixin

  ```SerializerMixin``` comes from flask-sqlalchemy-serializer — it's a shortcut that auto-generates a ```to_dict()``` method for you.

```bash
pipenv install flask-sqlalchemy-serializer
```


3. Migration
In server folder

install flask-migrate

```bash
pipenv install flask-migrate
```

## Step 1: Initialize migrations
```bash
flask db init
```


## Step 2: Create the 1st migration

```bash
flask db migrate -m "initial models"
```

## Step 3: Migrate to the database

```bash
flask db upgrade
```
