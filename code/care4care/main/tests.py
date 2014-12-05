from django.test import TestCase
from django.utils import timezone
from main.models import MemberType, STATUS, ACTIVE

class SimpleTestCase(TestCase):
    def setUp(self):
        pass

    def test_1plus1(self):
        self.assertEqual(1+1, 2)

class UserTestCase(TestCase):

    @classmethod
    def setUp(self):
        user = User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

    def get_full_name_test(self):
        self.assertEqual(user.get_full_name, "first_test last_test")

    def check_default_user_type(self):
        self.assertEqual(user.user_type, MemberType.MEMBER)

    def check_default_credit(self):
        self.assertEqual(user.credit,0)

    def check_default_status(self):
        self.assertEqual(user.status, ACTIVE)

    def check_default_verified(self):
        self.assertEqual(user.is_verified, False)

    def login_user_with_correct_info(self):
        success = user.login(username='username_test', password='secret')
        self.assertEqual(success,True)

class UserFavoriteTestCase(TestCase):

    @classmethod
    def setUp(self):
        user = User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

        user2 = User.objects.create(first_name="first_test2", last_name="last_test2",\
        username="username_test2",birth_date=timezone.now(),how_found=0,\
        email="test2@test.com", password="test2")

    def add_favorite(self):
        user.favorites.add(user2)
        self.assertEqual(user.favorites.contains(user2), True)

    def remove_favorite(self):
        user.favorites.remove(user2)
        self.assertEqual(user.favorites.contains(user2), False)
