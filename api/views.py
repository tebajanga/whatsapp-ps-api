from django.shortcuts import render
from rest_framework import generics
from .serializers import InboxSerializer, OutboxSerializer
from .models import Inbox, Outbox

class InboxCreateView(generics.ListCreateAPIView):
    """ Create function of the API """
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer

    def perform_create(self, serializer):
        """ Save the post data when creating new inbox message """
        serializer.save()


class OutboxCreateView(generics.ListCreateAPIView):
    """ """
    queryset = Outbox.objects.all()
    serializer_class = OutboxSerializer

    def perform_create(self, serializer):
        """ """
        serializer.save()
