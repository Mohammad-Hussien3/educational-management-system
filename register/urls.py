from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/', views.LogIn.as_view()),
    path('getrequests/', views.GetRequests.as_view()),
    path('replyuser/<int:pk>/<int:state>/', views.ReplyUser.as_view()),
    path('getallusers/', views.GetAllUsers.as_view()),
    path('getprofile/<int:id>/', views.GetProfile.as_view()),
    path('editfirstname/<int:id>/', views.EditFirstName.as_view()),
    path('editlastname/<int:id>/', views.EditLastName.as_view()),
    path('editpassword/<int:id>/', views.EditPassword.as_view()),
    path('logiut/<int:id>/', views.LogIn.as_view()),
]