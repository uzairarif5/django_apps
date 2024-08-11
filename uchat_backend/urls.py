from django.urls import path
from . import views

urlpatterns = [
  path("authorize", views.authorize),
  path("get_token", views.get_token),
  path("send_message", views.send_message)
]