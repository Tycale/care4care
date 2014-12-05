from django.test import TestCase
from django.utils import timezone
from main.models import MemberType, STATUS, ACTIVE
from main.models import User
from django.contrib.auth import authenticate, login as _login

class UserFullNameTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

    def test_get_full_name_test(self):
        user = User.objects.get(first_name="first_test")
        self.assertEqual(user.get_full_name(), "first_test last_test")

class UserDefaultTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

    def test_check_default(self):
        user = User.objects.get(first_name="first_test")
        self.assertEqual(user.user_type, MemberType.MEMBER)
        self.assertEqual(user.credit,0)
        self.assertEqual(user.status, ACTIVE)
        self.assertEqual(user.is_verified, False)

class UserAddFavoriteTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

        User.objects.create(first_name="first_test2", last_name="last_test2",\
        username="username_test2",birth_date=timezone.now(),how_found=0,\
        email="test2@test.com", password="test2")

    def test_add_favorite(self):
        user = User.objects.get(first_name="first_test")
        user2 = User.objects.get(first_name="first_test2")
        user.favorites.add(user2)
        self.assertEqual(user.favorites.filter(pk=user2.id).count(), 1)

class UserRemoveFavoriteTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

        User.objects.create(first_name="first_test2", last_name="last_test2",\
        username="username_test2",birth_date=timezone.now(),how_found=0,\
        email="test2@test.com", password="test2")

    def test_remove_favorite(self):
        user = User.objects.get(first_name="first_test")
        user2 = User.objects.get(first_name="first_test2")
        user.favorites.remove(user2)
        self.assertEqual(user.favorites.filter(pk=user2.id).count(), 0)

class UserAddNetworkTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

        User.objects.create(first_name="first_test2", last_name="last_test2",\
        username="username_test2",birth_date=timezone.now(),how_found=0,\
        email="test2@test.com", password="test2")

    def test_add_network(self):
        user = User.objects.get(first_name="first_test")
        user2 = User.objects.get(first_name="first_test2")
        user.personal_network.add(user2)
        self.assertEqual(user.personal_network.filter(pk=user2.id).count(), 1)

class UserRemoveNetworkTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

        User.objects.create(first_name="first_test2", last_name="last_test2",\
        username="username_test2",birth_date=timezone.now(),how_found=0,\
        email="test2@test.com", password="test2")

    def test_remove_network(self):
        user = User.objects.get(first_name="first_test")
        user2 = User.objects.get(first_name="first_test2")
        user.personal_network.remove(user2)
        self.assertEqual(user.personal_network.filter(pk=user2.id).count(), 0)

class UserIgnoreTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

        User.objects.create(first_name="first_test2", last_name="last_test2",\
        username="username_test2",birth_date=timezone.now(),how_found=0,\
        email="test2@test.com", password="test2")

    def test_add_ignore(self):
        user = User.objects.get(first_name="first_test")
        user2 = User.objects.get(first_name="first_test2")
        user.ignore_list.add(user2)
        self.assertEqual(user.ignore_list.filter(pk=user2.id).count(), 1)

    def test_remove_ignore(self):
        user = User.objects.get(first_name="first_test")
        user2 = User.objects.get(first_name="first_test2")
        user.ignore_list.remove(user2)
        self.assertEqual(user.ignore_list.filter(pk=user2.id).count(), 0)
