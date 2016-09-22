# noinspection PyPep8Naming
from unittest import TestCase

from django.contrib.auth.models import User
from django.db.models import Q

from dtrprofile.models_flag import UserFlag, USERFLAG_TYPES


class UserFlagTestCase(TestCase):

    def setUp(self):
        n1, p1, m1 = 'oieyriiwhbv', 'hunter2', 'testuser1@example.com'
        n2, p2, m2 = '8hfwieuhfvv', 'hunter2', 'testuser2@example.com'
        self.user1 = User.objects.create_user(n1, email=m1, password=p1)
        self.user2 = User.objects.create_user(n2, email=m2, password=p2)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_get_flag_type(self):
        for fo in USERFLAG_TYPES:
            flag_name = fo[1]
            flag_item = UserFlag.get_flag_type(flag_name)
            flag_type = flag_item[0]
            self.assertEqual(fo[0], flag_type)
        # And this one should not exist
        self.assertRaises(IndexError, UserFlag.get_flag_type, 'fdgkfhgPMq')

    def test_friends_flag(self):
        """Using UserFlag methods, create a 'friends' relation between two
        users, then delete the relation again, test every step.

        Two way flags: this is the same as below `test_like_flag()`, but keep
        as separate test methods to make it more obvious where errors are.
        """
        flag_name = 'friend'
        flag_type = UserFlag.get_flag_type(flag_name)[0]

        # Have user1 send a friend invite to user2
        UserFlag.set_flag(flag_name, self.user1, self.user2)
        # Verify there is an "invited" entry in UserFlag
        f = UserFlag.objects.filter(sender=self.user1, receiver=self.user2,
                                    flag_type=flag_type)
        self.assertEqual(f.count(), 1, msg='should find exactly one entry')
        self.assertEqual(f.first().confirmed, None, msg='shoud be unconfirmed')

        # Have user2 confirm the open invite
        UserFlag.set_flag(flag_name, self.user2, self.user1)
        # Verify there is a confirmed friends entry in UserFlag
        f = UserFlag.get_two_way_flags(self.user1, self.user2)
        f = f.filter(flag_type=flag_type)  # only filter 'friends' flags
        self.assertEqual(f.count(), 1, msg='should find exactly one entry')
        self.assertNotEqual(f.first().confirmed, None, msg='should be confirm.')

        # Have user1 cancel the 'friends' flag
        UserFlag.remove_flag(flag_name, self.user1, self.user2)
        # Verify there is no confirmed friends entry in UserFlag
        f = UserFlag.get_two_way_flags(self.user1, self.user2)
        f = f.filter(flag_type=flag_type)  # only filter 'friends' flags
        self.assertEqual(f.count(), 1, msg='should find one entry')
        self.assertEqual(f.first().confirmed, None, msg='should be unconfirmed')

        # Have user2 cancel the 'friends' flag, too
        UserFlag.remove_flag(flag_name, self.user2, self.user1)
        # Verify there is no 'friends' entry for the users.
        f = UserFlag.objects.filter((Q(sender=self.user1, receiver=self.user2) |
                                     Q(sender=self.user2, receiver=self.user1)),
                                    flag_type=flag_type)
        self.assertEqual(f.count(), 0, msg='should find no entries')

    def test_like_flag(self):
        """Using UserFlag methods, user1 creates a 'like' on user2, then user2
        likes back to create a match, then user1 removes the like, then user2
        removes the like. Test every step."""
        flag_name = 'like'
        flag_type = UserFlag.get_flag_type(flag_name)[0]

        # Set user1 'likes' user2
        UserFlag.set_flag('like', self.user1, self.user2)
        # Verify the 'like' is set
        f = UserFlag.objects.filter(sender=self.user1, receiver=self.user2,
                                    flag_type=flag_type)
        self.assertEqual(f.count(), 1, msg='should find exactly one entry')
        self.assertEqual(f.first().confirmed, None, msg='shoud be unconfirmed')

        # Have user2 'like' user1 back.
        UserFlag.set_flag(flag_name, self.user2, self.user1)
        # Verify there is a match
        f = UserFlag.get_two_way_flags(self.user1, self.user2)
        f = f.filter(flag_type=flag_type)
        self.assertEqual(f.count(), 1, msg='should find exactly one entry')
        self.assertNotEqual(f.first().confirmed, None, msg='should be confirm.')

        # Have user1 cancel the 'like' flag
        UserFlag.remove_flag(flag_name, self.user1, self.user2)
        # Verify there is no match, but user2 'likes' user1
        f = UserFlag.get_two_way_flags(self.user1, self.user2)
        f = f.filter(flag_type=flag_type)
        self.assertEqual(f.count(), 1, msg='should find one entry')
        self.assertEqual(f.first().confirmed, None, msg='should be unconfirmed')

        # Have user2 remove the 'like' flag, too
        UserFlag.remove_flag(flag_name, self.user2, self.user1)
        # Verify there is no 'friends' entry for the users
        f = UserFlag.objects.filter((Q(sender=self.user1, receiver=self.user2) |
                                     Q(sender=self.user2, receiver=self.user1)),
                                    flag_type=flag_type)
        self.assertEqual(f.count(), 0, msg='should find no entries')

    def test_one_way_flag(self):
        for flag_name in ['block', 'favorite', 'viewed']:
            flag_type = UserFlag.get_flag_type(flag_name)[0]

            # Set user1 sets flag on user2
            UserFlag.set_flag(flag_name, self.user1, self.user2)
            # Verify "manually" the flag is set
            f = UserFlag.objects.filter(sender=self.user1, receiver=self.user2,
                                        flag_type=flag_type)
            self.assertEqual(f.count(), 1, msg='should find exactly one entry')

            # Have user1 cancel the flag
            UserFlag.remove_flag(flag_name, self.user1, self.user2)
            # Verify there is no flag
            f = UserFlag.get_one_way_flags(self.user1, self.user2)
            f = f.filter(flag_type=flag_type)
            self.assertEqual(f.count(), 0, msg='should find no entry')
