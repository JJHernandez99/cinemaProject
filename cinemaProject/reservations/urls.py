from django.conf.urls import url
from reservations import views

urlpatterns = [
    url(r'^api/peliculas$', views.peliculas_list),
    ]