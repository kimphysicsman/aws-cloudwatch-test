from django.urls import path

from .views import LogView, HomeView, OpenSearchView

urlpatterns = [
    path('', LogView.as_view()),
    path('opensearch', OpenSearchView.as_view()),
    path('home', HomeView.as_view()),
]
