from django.test import TestCase
from django.utils import timezone
from main.models import MemberType, STATUS, ACTIVE
from main.models import User
from django.contrib.auth import authenticate, login as _login
from django.test.client import Client, RequestFactory


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

class UserLoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

    def test_login_user_with_correct_info(self):
        login = self.client.login(username=self.user.username, password="test")
        self.assertEqual(login, True)

    def test_login_user_with_incorrect_info(self):
        login = self.client.login(username="username_test", password="bidon")
        self.assertEqual(login, False)

class UserAccountTypeVerboseTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

    def test_check_verbose_m(self):
        self.assertEqual(self.user.get_account_type(), MemberType.VERBOSE_M)

    def test_check_verbose_nm(self):
        self.user.user_type = MemberType.NON_MEMBER
        self.user.save()
        self.assertEqual(self.user.get_account_type(), MemberType.VERBOSE_NM)

    def test_check_verbose_vm(self):
        self.user.user_type = MemberType.VERIFIED_MEMBER
        self.user.save()
        self.assertEqual(self.user.get_account_type(), MemberType.VERBOSE_VM)

class UserCreditTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test", credit=60)

    def test_credit(self):
        self.assertEqual(self.user.get_verbose_credit(), "1 heure")

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

class UserEditTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

    def test_modify_status(self):
        self.user.email="coucou@coucou.be"
        self.user.save()
        self.assertEqual(self.user.email,"coucou@coucou.be")

class SuperUserCreationTestCase(TestCase):
    def setUp(self):
         self.super = User.objects.create_superuser(username="username_test",email="test@test.com", password="test")

    def test_super(self):
        self.assertEqual(self.super.is_superuser, True)

class UserLanguageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test", languages=["fr"])

    def test_verbose_lg(self):
        self.assertEqual(self.user.get_verbose_languages(), "Français")

class MainViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(first_name="first_test", last_name="last_test",\
        username="username_test",birth_date=timezone.now(),how_found=0,\
        email="test@test.com", password="test")

        def test_home(self):
            # Create an instance of a GET request.
            request = self.factory.get('home')

            request.user = self.user

            # Test my_view() as if it were deployed at /customer/details
            response = my_view(request)
            self.assertEqual(response.status_code, 200)

        def test_loggin(self):
            # Create an instance of a GET request.
            request = self.factory.get('login')

            request.user = self.user

            # Test my_view() as if it were deployed at /customer/details
            response = my_view(request)
            self.assertEqual(response.status_code, 200)
