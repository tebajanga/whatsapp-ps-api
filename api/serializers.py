from rest_framework import serializers
from .models import Inbox, Outbox

class InboxSerializer(serializers.ModelSerializer):
    """ Serializer to map the Model instance into JSON format. """

    class Meta:
        """ Meta class to map serializer's fields with the model fields."""
        model = Inbox
        fields = ('id', 'category', 'mimetype', 'sender', 'body','processed',
                    'processed_at')
        read_only_fields = ('created_at',)


class OutboxSerializer(serializers.ModelSerializer):
    """ Serializer to map the Model instance into JSON format. """

    class Meta:
        """ Meta class to map serializer's fields with the model fields."""
        model = Outbox
        fields = ('id', 'category', 'mimetype', 'receiver', 'chat_found', 'body',
                'processed', 'processed_at')
        read_only_fields = ('created_at',)
