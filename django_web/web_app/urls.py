from django.urls import path

from web_app.views import home

urlpatterns = [
    path('', home)
]
