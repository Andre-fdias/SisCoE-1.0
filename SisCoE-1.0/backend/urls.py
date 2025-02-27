from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('backend.core.urls', namespace='core')),  # noqa E501
    path('admin/', admin.site.urls),  # noqa E501
    path('crm/', include('backend.crm.urls', namespace='crm')),  # noqa E501
    path('efetivo/', include('backend.efetivo.urls', namespace='efetivo')),  # noqa E501
    path('adicional/', include('backend.adicional.urls', namespace='adicional')),  # noqa E501
    path('accounts/', include('backend.accounts.urls')),  # noqa E501
    path('faisca/', include('backend.faisca.urls', namespace='faisca')),  # noqa E501
    path('rpt/', include('backend.rpt.urls', namespace='rpt')),  # noqa E501
    path('bm/', include('backend.bm.urls', namespace='bm')),  # noqa E501
    path('municipios/', include('backend.municipios.urls', namespace='municipios')),  # noqa E501
    path('documentos/', include('backend.documentos.urls', namespace='documentos')),  # noqa E501

    path('agenda/', include('backend.agenda.urls', namespace='agenda')),  # noqa E501

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)