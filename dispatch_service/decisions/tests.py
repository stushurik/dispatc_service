"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime
from django.contrib.auth.models import User

from django.test import TestCase

from decisions.models import Decision
from events.models import Event


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='test')
        self.event = Event.objects.create(
            author=self.user,
            executor=self.user,
            description='description',
        )

    def test_create_decision(self):
        d = Decision.objects.create(
            author=self.user,
            description='description',
            deadline=datetime.datetime.today(),
            event=self.event
        )

        self.assertTrue(Decision.objects.filter(
            author=self.user,
            description='description',
            deadline=datetime.datetime.today(),
            event=self.event
        ).exists())

        self.assertEquals(d.author.id, self.user.id)
        self.assertEquals(d.description, 'description')
        self.assertEquals(d.deadline.day, datetime.datetime.today().day)
        self.assertEquals(d.event.id, self.event.id)

