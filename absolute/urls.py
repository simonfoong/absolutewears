from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views
# from home.sitemaps import StaticViewSitemap
from django.contrib.sites.models import Site
from django.views.generic import TemplateView


handler400 = 'home.views.handler400'
handler403 = 'home.views.handler403'
handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'


urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),
    path('', include('home.urls')),
    path('', include('store.urls')),
    path('', include('order.urls')),
    path('', include('users.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path('webpush/', include('webpush.urls')),
    

]


admin.site.index_title = "Absolute Wears"
admin.site.site_header = "Absolute Admin"
admin.site.site_title = "Absolute Admin"

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
