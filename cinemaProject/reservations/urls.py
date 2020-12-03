from django.conf.urls import url
from reservations import views

urlpatterns = [
    url(r'^api/peliculas$', views.peliculas_list),
    url(r'^api/peliculas/(?P<pk>[0-9]+)$', views.pelicula_detail),
    url(r'^api/salas$', views.salas_list),
    url(r'^api/salas/(?P<pk>[0-9]+)$', views.sala_detail),

    #url(r'^api/pelicula/(?P<pk_pelicula>[0-9]+)/sala/(?P<pk_sala>[0-9]+)/$', views.proyecciones_list),
    url(r'^api/proyecciones$', views.proyecciones_list),
    url(r'^api/proyecciones/(?P<fecha>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$)', views.proyecciones_list_range),
    #url(r'^api/butacas$', views.butacas_list),
    #url(r'^api/butacas/(?P<pk>[0-9]+)$', views.butaca_datail)
]