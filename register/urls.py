from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/', views.LogIn.as_view()),
    path('getrequests/', views.GetRequests.as_view()),
    path('replyuser/<int:pk>/<int:state>/', views.ReplyUser.as_view()),
    path('getallusers/', views.GetAllUsers.as_view()),
]