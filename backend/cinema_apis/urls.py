from django.urls import path
from . import views

urlpatterns=[
    path('top_5_movies/', views.MovieApi.as_view())
]