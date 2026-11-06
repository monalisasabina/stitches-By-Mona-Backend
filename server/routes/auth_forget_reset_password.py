from flask import request, current_app
from flask_restful import Resource
from flask_mail import Message

from datetime import datetime

from models import db
from models.admin import Admin

from extensions import mail

from utils.password_reset import generate_reset_token, verify_reset_token



#FORGET PASSWORD
class AdminForgotPassword(Resource):

    def post(self):

        data = request.get_json()

        email = data.get('email', '').strip().lower()

        if not email:
            return {
                'message': 'Please provide your email address.'
            }, 400

        # Look for an active administrator
        admin = Admin.query.filter_by(
            email=email,
            is_active=True
        ).first()

        # Always return a generic message.
        # This prevents people from discovering registered admin emails.
        response_message = (
            'If an active administrator account exists with that email, '
            'a password reset link will be sent.'
        )

        if not admin:
            return {
                'message': response_message
            }, 200

        # Generate reset token
        token = generate_reset_token(admin)

        # Build the frontend reset link
        reset_link = (
            f"{current_app.config['FRONTEND_URL']}"
            f"/admin/reset-password?token={token}"
        )

        # Prepare email
        message = Message(
            subject='Stitches by Mona - Password Reset',
            recipients=[admin.email]
        )

        message.body = f"""
Hello {admin.firstname},

We received a request to reset your Stitches by Mona administrator password.

Click the link below to reset your password:

{reset_link}

This link expires after 30 minutes.

If you did not request this password reset, you can ignore this email.

Regards,
Stitches by Mona
"""

        try:

            mail.send(message)

        except Exception:

            current_app.logger.exception(
                'Failed to send administrator password reset email.'
            )

        return {
            'message': response_message
        }, 200





# RESET PASSWORD
class AdminResetPassword(Resource):

    def post(self):

        data = request.get_json()

        token = data.get('token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check required fields
        if not token or not new_password or not confirm_password:

            return {
                'message': 'All fields are required.'
            }, 400

        # Check whether passwords match
        if new_password != confirm_password:

            return {
                'message': 'Passwords do not match.'
            }, 400

        # Password validation
        if len(new_password) < 8:

            return {
                'message': 'Password must contain at least 8 characters.'
            }, 400

        # Verify token
        token_data = verify_reset_token(token)

        if not token_data:

            return {
                'message': 'This password reset link is invalid or has expired.'
            }, 400

        # Find administrator
        admin = Admin.query.filter_by(
            id=token_data['admin_id'],
            is_active=True
        ).first()

        if not admin:

            return {
                'message': 'This password reset link is invalid or has expired.'
            }, 400

        # Check whether the password has changed since the token was generated
        current_timestamp = (
            admin.password_changed_at.isoformat()
            if admin.password_changed_at
            else None
        )

        if current_timestamp != token_data['password_changed_at']:

            return {
                'message': 'This password reset link is invalid or has expired.'
            }, 400

        # Update password
        admin.set_password(new_password)

        # Update timestamp to invalidate previously generated reset tokens
        admin.password_changed_at = datetime.utcnow()

        db.session.commit()

        return {
            'message': 'Your password has been reset successfully.'
        }, 200