from django.urls import path
from . import views

urlpatterns = [
    path('doctor/createexam/', views.CreateExam.as_view()),
    path('student/getallexams/<int:pk>/', views.GetAllExams.as_view()),
    path('student/solveexam/<int:pk>/', views.SolveExam.as_view()),
    path('doctor/getdoctorlist/<int:pk>/', views.GetDoctorList.as_view()),
    path('doctor/correctexam/', views.CorrectExam.as_view()),
    path('student/getstudentlist/<int:pk>/', views.GetStudentList.as_view()),
]