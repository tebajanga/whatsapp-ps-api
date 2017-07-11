from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import InboxCreateView,OutboxCreateView

urlpatterns = {
    url(r'^inboxes/$', InboxCreateView.as_view(), name='create'),
    url(r'^outboxes/$', OutboxCreateView.as_view(), name='create'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
