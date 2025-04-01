from django.conf.urls import url
from .views import listar_solicitudes, crear_solicitud, editar_solicitud, eliminar_solicitud, \
    SolicitudCreate, SolicitudDelete, SolicitudList, SolicitudUpdate

urlpatterns = [
    url(r'^cbv/solicitud/listar$', SolicitudList.as_view(), name='solicitud_listar'),
    url(r'^cbv/solicitud/nueva$', SolicitudCreate.as_view(), name='solicitud_crear'),
    url(r'^cbv/solicitud/editar/(?P<pk>\d+)/$', SolicitudUpdate.as_view(), name='solicitud_editar'),
    url(r'^cbv/solicitud/eliminar/(?P<pk>\d+)/$', SolicitudDelete.as_view(), name='solicitud_eliminar'),
    url(r'^func/solicitud/listar$', listar_solicitudes, name='solicitud_listar_func'),
    url(r'^func/solicitud/nueva$', crear_solicitud, name='solicitud_crear_func'),
    url(r'^func/solicitud/editar/(\d+)/$', editar_solicitud, name='solicitud_editar_func'),
    url(r'^func/solicitud/eliminar/(\d+)/$', eliminar_solicitud, name='solicitud_eliminar_func'),
]
