from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_email(mail, user):
    conf_code = default_token_generator.make_token(user)
    send_mail(
        subject="Confirmation Code",
        message=("Your confirmation code is: \n" f"{conf_code}"),
        from_email="support_bot@yamdb.com",
        recipient_list=[mail],
        fail_silently=True,
    )
