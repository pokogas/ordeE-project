from django.urls import path

from . import views
from .views import UserList

urlpatterns = [
    path('users/', UserList.as_view()),
    path('logout', views.BlacklistRefreshView.as_view(), name="logout"),
]
