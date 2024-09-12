from django.urls import path
from . import views

urlpatterns = [
    path('getmycourses/<int:id>/', views.GetMyCourses.as_view()),
    path('addcourse/<int:studentId>/<int:courseId>/', views.AddCourse.as_view()),
    path('createcourse/<int:doctorId>/', views.CreateCourse.as_view()),
    path('addexam/<int:courseId>/', views.AddExam.as_view()),
    path('addlecture/<int:courseId>/', views.AddLecture.as_view()),
]