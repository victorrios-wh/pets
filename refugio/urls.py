from django.conf.urls import include, url
from django.contrib import admin
from refugio.views import home

urlpatterns = [
    # Examples:
    # url(r'^$', 'refugio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^mascota/', include('apps.mascota.urls', namespace='mascota')),
    url(r'^adopcion/', include('apps.adopcion.urls', namespace='adopcion')),
]
