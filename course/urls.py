from django.urls import path
from . import views

urlpatterns = [
    path('getallcourses/<int:pk>/', views.GetAllCourses.as_view()),
    path('getmycourses/<int:pk>/', views.GetMyCourses.as_view()),
    path('addcourse/<int:doctorId>/', views.AddCourse.as_view()),
]