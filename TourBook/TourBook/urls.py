from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


api_patterns = [
    path('tours/', include('Tour_Organizer.urls', namespace='tour_organizer')),
    path('advertisers/', include('Advertiser.urls', namespace='advertiser')),
    path('clients/', include('Client.urls', namespace='client')),
    path('', include('Core.urls'), name='core'),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('api/', include(api_patterns)),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
