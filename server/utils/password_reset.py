from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app


# Generate a password-reset token
# Creates a signed token containing the administrators's ID and password-change timestamp
def generate_reset_token(admin):

    serializer = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY']
    )

    data = {
        'admin_id': admin.id,
        'password_changed_at': (
            admin.password_changed_at.isoformat()
            if admin.password_changed_at
            else None
        )
    }

    # creates a signed token containing the admin's ID
    # salt: separates password-reset tokens from other tokens your application might generate
    token = serializer.dumps(
        data,
        salt='admin-password-reset'
    )

    return token



# Verify a password-reset token
# Checks whether the token is valid and hasn't expired
def verify_reset_token(token):

    serializer = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY']
    )

    try:

        data = serializer.loads(
            token,
            salt='admin-password-reset',
            max_age=1800
        )

        # max_age=1800: making the token expire in 30minutes

        return data['admin_id']

    # checking if the token has expired or been modified
    except (SignatureExpired, BadSignature):
        return None