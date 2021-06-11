from django.urls import path

from . import views

urlpatterns = [
    path("page/index=<str:pk>/", views.WikiPage.as_view())
]