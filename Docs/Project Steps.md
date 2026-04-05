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
