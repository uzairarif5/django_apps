from django.urls import path

from . import views

urlpatterns = [
    path("getList", views.getList),
    path("allList", views.getAllList),
    path("handleStudyNotesForm", views.handleStudyNotesForm),
]