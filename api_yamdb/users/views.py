# from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from .models import User
from .serializers import UsersSerializer, UserRegistrationSerializer
import secrets
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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
        recipient_list=['to@example.com'],
        fail_silently=True,
    )
    return conf_code


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = send_email(request.data['email'])
        serializer.save(confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'


class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pass



# create jwt get token
# update jwt token