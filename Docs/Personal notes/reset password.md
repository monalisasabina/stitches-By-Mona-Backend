# FORGET/ RESET PASSWORD

## 1. How it works
1. Admin clicks "Forgot Password"
    On the admin login page, they enter their registered email address.


2. Backend generates a secure reset token
    Flask creates a temporary token and sends a reset link to the admin's email.


3. Admin opens the reset link
    The link takes them to a React page where they enter a new password.


4. Backend validates the token
    Flask checks that the token is valid and hasn't expired.


5. Password is updated
    Flask hashes the new password and saves it. The admin can then log in normally.

---    


## 2. itsdangerous

It is used for secure, time-limited reset tokens and email delivery through SMTP

It is a Python library created by the Pallets organization (the same team behind Flask and Werkzeug) used to safely pass cryptographically signed data to and from untrusted environments, such as HTTP cookies or URLs

```bash
pipenv install itsdangerous
```
---


## 3. Create the password-reset token helper

1. Create a folder  called ```utils```

2. Create 2 files:

```bash
utils/
├── __init__.py
└── password_reset.py
```

Check ```password_reset.py``` for the contents. ```__init.py``` is left blank..

---


### 4. Install Flask-Mail

1. Run
```bash
pipenv install Flask-Mail
```

2. In ```config.py``` add;

```python

    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

```


3. In ```.env``` add;

```bash

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

```

4. Create a file called ```extension.py``` in server directory:

```Python

from flask_mail import Mail

mail = Mail()

```

In ```run.py```:

```python

from extensions import mail

def create_app()

    ....

    app.config.from_object(Config)

    mail.init_app(app)

    ....

```

5. Creating the routes

Create ```auth_forget_reset_password.py``` file. Check the file for the code. 
It should contain both the ```forget password resource``` and ```reset password resource```

In ```run.py```:

```python

    from routes.auth_forget_reset_password import AdminForgotPassword, AdminResetPassword
    api.add_resource(AdminForgotPassword, '/auth/admin/forgot-password')
    api.add_resource(AdminResetPassword, '/auth/admin/reset-password')

```




 




