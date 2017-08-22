from django.shortcuts import render
from rest_framework import generics
from .serializers import InboxSerializer, OutboxSerializer,InboxPostSerializer,OutboxPostSerializer
from .models import Inbox, Outbox
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)

class OutboxCreateView(generics.ListCreateAPIView):
    """ """
    queryset = Outbox.objects.all()
    serializer_class = OutboxSerializer

    def perform_create(self, serializer):
        """ """
        serializer.save()

class OutboxDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles GET, PUT and DELETE requests """
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def inbox(request, pk=None):
    """
    Retrieve inbox messages, default limit 50 and create new inbox message
    on a post request
    POST parameters:
        sender, category, mimetype, body
    """
    limit = 50
    if request.method == 'GET':
        inboxes = Inbox.objects.filter(processed=False)[:limit]
        if inboxes:
            serializer = InboxSerializer(inboxes, many=True)
            response = {'status': 200, 'description': 'Success',
                'messages': serializer.data
            }
        else:
            response = {
                'status': 404, 'description': 'There are no inbox messages'
            }
        return Response(response)


    if request.method == 'POST':

        serializer = InboxPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #print serializer.data
            response = {
                'status': 200, 'description': 'Success', 'message_id': serializer.data['id']
            }
        else:
            response = {
                'status': 500, 'description': 'Invalid input data'
            }
        return Response(response)


    if request.method == 'PUT':
        try:
            inbox = Inbox.objects.get(pk=pk)
            inbox.processed_at = timezone.now().date()
            serializer = InboxSerializer(inbox, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': 200,
                    'description': 'Success',
                    'message_id': serializer.data['id']
                }
            else:
                response = {
                    'status':  200,
                    'description': 'No changes'
                }
        except Exception as e:
            response = {
                'status': 404,
                'description': 'Message with ID:{} was not found'.format(pk)
            }


        return Response(response)

    if request.method == 'DELETE':
        try:
            inbox = Inbox.objects.get(pk=pk)
            result = inbox.delete()
            print result;

            response = {
                'status': 200,
                'description': 'Message deleted'
            }
        except Exception as e:

            response = {
                'status': 404,
                'description': 'Message with ID:{} was not found'.format(pk)
            }
        return Response(response)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def outbox(request, pk=None):
    """
    Retrieve outbox messages, default limit 50 and create new outbox message
    on a post request
    POST parameters:
        receiver, category, mimetype, body
    """
    limit = 50
    if request.method == 'GET':
        outboxes = Outbox.objects.filter(processed=False)[:limit]
        if outboxes:
            serializer = OutboxSerializer(outboxes, many=True)
            response = {'status': 200, 'description': 'Success',
                'messages': serializer.data
            }
        else:
            response = {
                'status': 404, 'description': 'There are no outbox messages'
            }
        return Response(response)


    if request.method == 'POST':

        serializer = OutboxPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #print serializer.data
            response = {
                'status': 200, 'description': 'Success', 'message_id': serializer.data['id']
            }
        else:
            response = {
                'status': 500, 'description': 'Invalid input data'
            }
        return Response(response)


    if request.method == 'PUT':
        try:
            outbox = Outbox.objects.get(pk=pk)
            outbox.processed_at = timezone.now().date()
            serializer = OutboxSerializer(outbox, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': 200,
                    'description': 'Success',
                    'message_id': serializer.data['id']
                }
            else:
                response = {
                    'status':  200,
                    'description': 'No changes'
                }
        except Exception as e:
            print e
            response = {
                'status': 404,
                'description': 'Message with ID:{} was not found'.format(pk)
            }


        return Response(response)

    if request.method == 'DELETE':
        try:
            outbox = Outbox.objects.get(pk=pk)
            result = outbox.delete()
            response = {
                'status': 200,
                'description': 'Message deleted'
            }
        except Exception as e:

            response = {
                'status': 404,
                'description': 'Message with ID:{} was not found'.format(pk)
            }
        return Response(response)


@api_view(["POST", "GET"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    logger.info('Authenticating user...')
    print 'Auth user...'
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})
