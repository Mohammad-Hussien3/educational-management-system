from django.urls import path
from . import views

urlpatterns = [
    path('getmycourses/<int:id>/', views.GetMyCourses.as_view()),
    path('addcourse/<int:studentId>/<int:courseId>/', views.AddCourse.as_view()),
    path('createcourse/<int:doctorId>/', views.CreateCourse.as_view()),
    path('addexam/<int:courseId>/', views.AddExam.as_view()),
    path('addlecture/<int:courseId>/', views.AddLecture.as_view()),
    path('getpage/<int:courseId>/<int:studentId>/<int:pageIndex>/', views.GetPage.as_view()),
    path('getcourses/<int:studentId>/', views.GetCourses.as_view()),
    path('courseregister/<int:courseId>/<int:studentId>/', views.CourseRegister.as_view()),
    path('getallregisterrequests/<int:doctorId>/', views.GetAllRegisterRequests.as_view()),
    path('acceptregisterrequest/<int:courseId>/<int:studentId>/', views.AcceptRegisterRequest.as_view()),
]