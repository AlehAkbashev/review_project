from rest_framework import status
from .serializers import UserRegistrationSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .service import send_email
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    try:
        user = User.objects.get(
            email=request.data['email'],
            username=request.data['username']
        )
        send_email(request.data['email'], user)
        return Response(
            request.data,
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.data['email']
        username = serializer.data['username']
        user = User.objects.get(
            email=email,
            username=username
        )
        send_email(request.data['email'], user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )
