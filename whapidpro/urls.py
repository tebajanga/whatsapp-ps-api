from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import whapidpro_pusher

urlpatterns = {
    url(r'^whapidpro\/push$', whapidpro_pusher, name='whapidpro_pusher'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
