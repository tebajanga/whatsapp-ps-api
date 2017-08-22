from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.cache import cache
import logging
from api.models import Inbox, Outbox
from django.conf import settings

logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def whapidpro_pusher(request):
    print request.data
    jo = '+255766266161'
    processed = 1
    unprocessed = 0
    failed = 2
    pending = 3
    default_mimetype = 'text'
    sender = request.data['to']
    sender_cache = cache.get(sender)

    running_flow = None

    if sender_cache:
        #update the last message
        original_message = Inbox.objects.filter(processed=unprocessed, sender=sender).last()
        print sender_cache
        if original_message:
            if 'last_message' in sender_cache.keys() and original_message.id == sender_cache['last_message']:
                original_message.processed = processed
                original_message.save()

            else:
                original_message.processed = pending
                original_message.save()
            #del sender_cache['last_message']
        running_flow = sender_cache['flow']
    else:
        #ToDo update cache setting...try to trigger a flow
        pass


    outbox = Outbox()
    outbox.receiver = request.data['to']
    outbox.body = request.data['text']
    cat_flow_settings = settings.CATEGORY_FLOW_MAP
    if running_flow:
        category = cat_flow_settings.keys()[cat_flow_settings.values().index(running_flow)]
    else:
        category = cat_flow_settings.keys()[0]

    outbox.category = category
    outbox.mimetype = default_mimetype
    outbox.save()
    logger.info('Saved outbound message ID:{}'.format(outbox.id))
    return HttpResponse("OK")
