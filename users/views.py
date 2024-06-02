from .models import User
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from .serializers import (
    UserSerializer, 
    UserUpdateSerializer, 
    RegisterSerializer, 
    ChangePasswordSerializer
)
from .permissions import IsAdminOrIsSelf


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

class UserViewRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrIsSelf]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_staff or obj == self.request.user:
            return obj
        else:
            raise PermissionDenied("You do not have permission to perform this action.")

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *arg, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
class LogoutView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
            data = {
            "message" : "Successfully logged out..."
        }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "message": "No active session found."
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def reset_password(request):
    email = request.data["email"]

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        send_mail(
            "Your New Password",
            "Your New Password is " + password,
            'kadir.ozcelik16@gmail.com',
            [email],
            fail_silently=False
        )
        return Response({"message" : "Your Password Reset Succesfully"}, status=status.HTTP_200_OK)

    else:
        return Response({"message" : "No such email address exists"}, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            request.user.auth_token.delete()
            return Response({"message" : "Your password successfully changed."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



