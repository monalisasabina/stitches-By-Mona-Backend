## 1. Install dependancies

```bash
pipenv install flask-jwt-extended bcrypt
```

## 2. Update ```config/py```

```python

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY                  = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI     = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY              = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES    = timedelta(days=1)     # customers

```

## 3. Update ```.env```

```bash
SECRET_KEY=<first output here>
DATABASE_URL=sqlite:///stitches.db
JWT_SECRET_KEY=<second output here>
FLASK_APP=run.py
FLASK_ENV=development
```

## 4. Generate code for the keys

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 5. Generate 8 random codes

```bash
python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8)))"
```