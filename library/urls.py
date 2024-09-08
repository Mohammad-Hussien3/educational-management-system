from django.urls import path
from . import views

urlpatterns = [
    path('getarticles/', views.GetArticles.as_view()),
    path('addarticle/', views.AddArticle.as_view()),
]