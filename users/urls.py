from django.urls import path
from .views import (
    UserView, 
    UserViewRUD, 
    RegisterView, 
    CustomAuthToken, 
    LogoutView
)

urlpatterns = [
    path('users/', UserView.as_view()),
    path('user/<int:pk>/', UserViewRUD.as_view()),
    path('addnewuser/', RegisterView.as_view(), name="addnewuser"),
    path('login/', CustomAuthToken.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),   
]