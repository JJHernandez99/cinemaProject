from django.conf.urls import url
from reservations import views

urlpatterns = [
    url(r'^api/peliculas$', views.peliculas_list),
    #url(r'^api/peliculas/(?P<pk>[0-9]+)$', views.pelicula_delete),
    url(r'^api/peliculas/(?P<pk>[0-9]+)/(?P<fechaI>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)/'
        r'(?P<fechaF>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$)', views.pelicula_detail),
    url(r'^api/salas$', views.salas_list),
    url(r'^api/salas/(?P<pk>[0-9]+)$', views.sala_detail),
    url(r'^api/proyecciones/(?P<pk>[0-9]+)$', views.proyeccion_detail),
    url(r'^api/proyecciones$', views.proyecciones_list),
    url(r'^api/proyecciones/(?P<fecha>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$)',
        views.proyecciones_list_range),
    url(r'^api/proyecciones/(?P<pk>[0-9]+)/(?P<fecha>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$)',
        views.proyeccion_detail_range),
    url(r'^api/butacas$', views.butacas_list),
    url(r'^api/butacas/(?P<pk>[0-9]+)$', views.butaca_detail),
    url(r'^api/reportes/butacas/(?P<fechaI>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)/'
        r'(?P<fechaF>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$)', views.reporte_butacas),
    url(
        r'^api/reportes/butacas/(?P<pk>[0-9]+)/(?P<fechaI>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)/'
        r'(?P<fechaF>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$)',
        views.reporte_butacas_proyeccion),
    url(r'^api/reportes/proyecciones/(?P<fechaI>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)/'
        r'(?P<fechaF>(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$)',
        views.reporte_ranking_proyecciones),
    url(r'^api/reportes/peliculas$', views.reporte_entradas_peliculas)
]
