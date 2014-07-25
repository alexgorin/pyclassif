from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.db.models.loading import cache as model_cache
if not model_cache.loaded:
    model_cache.get_models()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('recognition.urls')),
    url(r'^recognition/', include('recognition.urls')),
)
