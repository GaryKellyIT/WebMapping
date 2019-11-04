from django.urls import path

from polls import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
]