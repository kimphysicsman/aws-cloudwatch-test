from django.urls import path

from .views import LogView, HomeView

urlpatterns = [
    path('', LogView.as_view()),
    path('home', HomeView.as_view()),
]
