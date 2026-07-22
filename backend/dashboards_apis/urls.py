from django.urls import path
from . import views

urlpatterns=[
    path("exective-dashboard/", views.DashboardApi.as_view(), name='executive-dashboard')
]