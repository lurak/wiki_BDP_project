from django.urls import path

from . import reports_view

urlpatterns = [
    path("top_twenty/", reports_view.WikiReportTopTwenty.as_view()),
    path("by_hours/", reports_view.WikiReportByHours.as_view()),
    path("bots_six_hours/", reports_view.WikiReportBotSixHours.as_view())
]
