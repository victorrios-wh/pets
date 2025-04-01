from django.conf.urls import url
from .views import SolicitudCreate, SolicitudDelete, SolicitudList, SolicitudUpdate

urlpatterns = [
    url(r'^cbv/solicitud/listar$', SolicitudList.as_view(), name='solicitud_listar'),
    url(r'^cbv/solicitud/nueva$', SolicitudCreate.as_view(), name='solicitud_crear'),
    url(r'^cbv/solicitud/editar/(?P<pk>\d+)/$', SolicitudUpdate.as_view(), name='solicitud_editar'),
    url(r'^cbv/solicitud/eliminar/(?P<pk>\d+)/$', SolicitudDelete.as_view(), name='solicitud_eliminar'),
]
