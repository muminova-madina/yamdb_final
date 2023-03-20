from django.contrib.auth.tokens import PasswordResetTokenGenerator

account_access_token = PasswordResetTokenGenerator()


def send_email(user):
    token = account_access_token.make_token(user)
    subject = 'Activate Your YAMDB Account'
    message = (
        f'Привет {user.username}, \n Спасибо за использование YAMDB.'
        f'\n Твой код подтверждения {token}'
    )
    user.email_user(subject, message)
