from django.conf.urls import url
from .views import mascota_delete, mascota_edit, mascota_list, mascota_view,\
    MascotaCreate, MascotaDelete, MascotaList, MascotaUpdate

urlpatterns = [
    url(r'^cbv/nuevo$', MascotaCreate.as_view(), name='mascota_crear'),
    url(r'^cbv/listar$', MascotaList.as_view(), name='mascota_listar'),
    url(r'^cbv/editar/(?P<pk>\d+)/$', MascotaUpdate.as_view(), name='mascota_editar'),
    url(r'^cbv/eliminar/(?P<pk>\d+)/$', MascotaDelete.as_view(), name='mascota_eliminar'),
    url(r'^func/nuevo$', mascota_view, name='mascota_crear_func'),
    url(r'^func/listar$', mascota_list, name='mascota_listar_func'),
    url(r'^func/editar/(\d+)/$', mascota_edit, name='mascota_editar_func'),
    url(r'^func/eliminar/(\d+)/$', mascota_delete, name='mascota_eliminar_func'),
]
