import datetime
import os

from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import CustomUser


class TestUserModels(TestCase):
    def setUp(self):
        self.user = CustomUser(
            username='groot',
            first_name='test1',
            last_name='test2',
            email='test@test.com',
            birth_date=datetime.datetime.now() + datetime.timedelta(days=5),
        )
        self.user.save()

    def test_birth_date(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_add_friend(self):
        friend = CustomUser(
            username='friend',
            first_name='friend',
            last_name='friend',
            email='friend@friend.com',
            birth_date=datetime.datetime.now() + datetime.timedelta(days=5),
        )
        friend.save()
        friend.friends.add(self.user)
        self.assertIn(friend, self.user.friends.all())