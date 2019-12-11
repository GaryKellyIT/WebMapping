from django.urls import path

from polls import views
from polls.views import MapPage

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('func', views.get_amenities, name='func'),
]
