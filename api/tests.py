from django.test import TestCase
from .models import Inbox, Outbox
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.renderers import JSONRenderer
from .serializers import InboxSerializer

class InboxTestCase(TestCase):
    """ Test Inbox model """

    def setUp(self):
        self.sender = '25576626161'
        self.category = 'afya'
        self.mimetype = 'text',
        self.body= 'Test message',
        self.processed = 0
        self.inbox = Inbox(sender=self.sender, category=self.category,
                            mimetype=self.mimetype, body=self.body)


    def test_create_inbox_message(self):
        old_count = Inbox.objects.count()
        self.inbox.save()
        new_count = Inbox.objects.count()
        self.assertNotEqual(old_count, new_count)



class OutBoxTestCase(TestCase):
    """ Test Outbox model """

    def setUp(self):
        self.receiver = '25576626161'
        self.category = 'afya'
        self.mimetype = 'text',
        self.body= 'Test message',
        self.processed = 0
        self.outbox = Outbox(receiver=self.receiver, category=self.category,
                            mimetype=self.mimetype, body=self.body)


    def test_create_inbox_message(self):
        old_count = Outbox.objects.count()
        self.outbox.save()
        new_count = Outbox.objects.count()
        self.assertNotEqual(old_count, new_count)



class ViewTestCase(TestCase):
        """ Test suite for the api views. """

        def setUp(self):
            """ Test client and variables definition """
            self.client = APIClient()
            self.inbox_data = {'sender': '25576626161', 'category': 'afya',
                        'mimetype': 'text', 'body': 'Test message'}
            self.response = self.client.post(
                reverse('create'),
                self.inbox_data,
                format='json'
            )
            self.sender = '25576626161'
            self.category = 'afya'
            self.mimetype = 'text',
            self.body= 'Test message',
            self.processed = 0
            self.inbox = Inbox(sender=self.sender, category=self.category,
                                mimetype=self.mimetype, body=self.body)
            self.inbox.save()

        def test_api_create_inbox_message(self):
            self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        def test_api_get_inbox_message(self):
            """ Test for GET request on inbox message """
            inbox = Inbox.objects.get()
            response =  self.client.get(
                reverse('details',kwargs={'pk': inbox.id}),
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            #print InboxSerializer(instance=inbox).data, '*'*10, response
            #self.assertContains(response, InboxSerializer(instance=inbox).data)


        def test_api_update_inbox_message(self):
            """ Test for PUT request on inbox message """
            inbox = Inbox.objects.get()
            change_inbox = { "sender": '1234444', 'category': 'afya',
                        'mimetype':'text', 'body': ' Body'}
            res = self.client.put(
                reverse('details', kwargs={'pk': inbox.id}),
                change_inbox, format='json'
            )
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        def test_api_delete_inbox_message(self):
            """ Test DELETE request on inbox message """
            inbox = Inbox.objects.get()
            response = self.client.delete(
                reverse('details', kwargs={'pk': inbox.id}),
                format='json',
                follow=True
            )
            self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
