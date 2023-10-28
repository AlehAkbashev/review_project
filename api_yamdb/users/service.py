import secrets
from django.core.mail import send_mail


def send_email(mail):
    conf_code = secrets.token_hex(16)
    send_mail(
        subject='Confirmation Code',
        message=(
            'Your confirmation code is: \n'
            f'{conf_code}'
        ),
        from_email='support_bot@yamdb.com',
        recipient_list=[mail],
        fail_silently=True,
    )
    return conf_code
