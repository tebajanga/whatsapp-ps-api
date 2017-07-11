from django.test import TestCase
from .models import Inbox, Outbox
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse


class InboxTestCase(TestCase):

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

        def test_api_create_inbox_message(self):
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
