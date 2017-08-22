from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import OutboxCreateView,OutboxDetailsView, login
from rest_framework.authtoken import views

urlpatterns = {
    url(r'^login$', views.obtain_auth_token),
    url(r'^$', 'api.views.outbox', name='outbox'),
    url(r'^inbox/$', 'api.views.inbox', name='inbox'),
    url(r'^inbox/(?P<pk>[0-9]+)$', 'api.views.inbox', name='inbox'),
    url(r'^outbox/$', 'api.views.outbox', name='outbox'),
    url(r'^outbox/(?P<pk>[0-9]+)$', 'api.views.outbox', name='outbox'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
