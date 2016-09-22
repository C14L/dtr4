# noinspection PyPep8Naming
from datetime import timedelta
from unittest import TestCase

from django.contrib.auth.models import User
from django.utils.datetime_safe import date

from dtrprofile.models_flag import UserFlag
from dtrprofile.models_profile import UserProfile


class ProfileTestCase(TestCase):
    user = []

    def test_profile_is_created_and_deleted_with_user(self):
        n, p, m = 'dsgdjjfsghkf', 'hunter2', 'testuser@example.com'
        user = User.objects.create_user(n, email=m, password=p)
        user_id = user.id
        # Check if profile was created
        c = UserProfile.objects.filter(user_id=user_id).count()
        self.assertEqual(c, 1)
        # Delete user
        user.delete()
        # Check if profile was deleted
        c = UserProfile.objects.filter(user_id=user_id).count()
        self.assertEqual(c, 0)

    def test_get_friends(self):
        uli = [['oieyriiwhbv', 'hunter2', 'testuser1@example.com'],
               ['8hfwieuhfvv', 'hunter2', 'testuser2@example.com'],
               ['Opc8s9nsdfb', 'hunter2', 'testuser3@example.com']]
        for u in uli:
            user = User.objects.create_user(u[0], email=u[2], password=u[1])
            self.user.append(user)
        # Set user[0] to be 'friends' with both user[1] and user[2]
        UserFlag.set_flag('friend', self.user[0], self.user[1])
        UserFlag.set_flag('friend', self.user[0], self.user[2])
        UserFlag.set_flag('friend', self.user[1], self.user[0])
        UserFlag.set_flag('friend', self.user[2], self.user[0])
        self.assertEqual(len(self.user[0].profile.get_friends()), 2)
        UserFlag.remove_flag('friend', self.user[0], self.user[1])
        self.assertEqual(len(self.user[0].profile.get_friends()), 1)
        UserFlag.remove_flag('friend', self.user[2], self.user[0])
        self.assertEqual(len(self.user[0].profile.get_friends()), 0)

    def test_get_age(self):
        n, p, m = 'dsgdjjfsghkf', 'hunter2', 'testuser@example.com'
        user = User.objects.create_user(n, email=m, password=p)
        user.profile.dob = date.today() - timedelta(days=int(356.25*21)-90)
        self.assertEqual(user.profile.get_age(), 20, msg='should be age 20')

