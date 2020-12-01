from django.conf.urls import url
from reservations import views

urlpatterns = [
    url(r'^api/peliculas$', views.peliculas_list),
    url(r'^api/salas$', views.salas_list),
    url(r'^api/salas/(?P<pk>[0-9]+)$', views.sala_detail),
]