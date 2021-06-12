from django.urls import path

from . import views

urlpatterns = [
    path("page/index=<str:pk>/", views.WikiPage.as_view()),
    path("domains/", views.WikiDomains.as_view()),
    path("user/index=<str:pk>/", views.WikiUser.as_view()),
    path("domain/name=<str:pk>/", views.WikiPagesByDomain.as_view()),
    path("time/start=<str:date_start>&end=<str:date_end>", views.WikiUsersByTime.as_view())
]