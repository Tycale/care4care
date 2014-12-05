from django.test import TestCase

from main.ajax.views import previous_month, next_month, month_list, \
                        get_days_in_month, \
                        get_users_registrated_json, get_account_types_json, \
                        get_users_status_json, get_job_categories_json, \
                        get_user_job_categories_json, get_user_job_avg_time_json, \
                        get_user_jobs_amount_json, get_user_time_amount_json, \
                        get_user_km_amount_json
from branch.models import Branch, Demand
from main.models import User, MemberType, ACTIVE, HOLIDAYS, UNSUBSCRIBE, \
                        JobCategory
from django.utils import timezone
import json



class Global_Registrated_Users_TestCase(TestCase):

    def test_users_registrated_json(self):
        empty = json.loads(get_users_registrated_json())
        data  = empty['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0, 0])

        User.objects.create(username='user1', first_name='First', last_name='User')
        one_user = json.loads(get_users_registrated_json())
        data = one_user['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0, 1])

        User.objects.create(username='user2', first_name='Second', last_name='User')
        two_users = json.loads(get_users_registrated_json())
        data = two_users['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0, 2])



class Global_Account_Types_TestCase(TestCase):

    def test_account_types_json(self):
        empty = json.loads(get_account_types_json())
        members = empty[0]['value']
        verif_members = empty[1]['value']
        non_members = empty[2]['value']
        self.assertEqual(members, 0)
        self.assertEqual(verif_members, 0)
        self.assertEqual(non_members, 0)

        User.objects.create(username='user1', user_type=MemberType.MEMBER)
        one_user = json.loads(get_account_types_json())
        members = one_user[0]['value']
        verif_members = one_user[1]['value']
        non_members = one_user[2]['value']
        self.assertEqual(members, 1)
        self.assertEqual(verif_members, 0)
        self.assertEqual(non_members, 0)


        User.objects.create(username='user2', user_type=MemberType.VERIFIED_MEMBER)
        two_users = json.loads(get_account_types_json())
        members = two_users[0]['value']
        verif_members = two_users[1]['value']
        non_members = two_users[2]['value']
        self.assertEqual(members, 1)
        self.assertEqual(verif_members, 1)
        self.assertEqual(non_members, 0)


        User.objects.create(username='user3', user_type=MemberType.NON_MEMBER)
        three_users = json.loads(get_account_types_json())
        members = three_users[0]['value']
        verif_members = three_users[1]['value']
        non_members = three_users[2]['value']
        self.assertEqual(members, 1)
        self.assertEqual(verif_members, 1)
        self.assertEqual(non_members, 1)



class Global_Users_Status_TestCase(TestCase):

    def test_users_status_json(self):
        empty = json.loads(get_users_status_json())
        actives = empty[0]['value']
        on_holiday = empty[1]['value']
        unsubscribed = empty[2]['value']
        self.assertEqual(actives, 0)
        self.assertEqual(on_holiday, 0)
        self.assertEqual(unsubscribed, 0)

        User.objects.create(username='user1', status=ACTIVE)
        one_user = json.loads(get_users_status_json())
        actives = one_user[0]['value']
        on_holiday = one_user[1]['value']
        unsubscribed = one_user[2]['value']
        self.assertEqual(actives, 1)
        self.assertEqual(on_holiday, 0)
        self.assertEqual(unsubscribed, 0)


        User.objects.create(username='user2', status=HOLIDAYS)
        two_users = json.loads(get_users_status_json())
        actives = two_users[0]['value']
        on_holiday = two_users[1]['value']
        unsubscribed = two_users[2]['value']
        self.assertEqual(actives, 1)
        self.assertEqual(on_holiday, 1)
        self.assertEqual(unsubscribed, 0)


        User.objects.create(username='user3', status=UNSUBSCRIBE)
        three_users = json.loads(get_users_status_json())
        actives = three_users[0]['value']
        on_holiday = three_users[1]['value']
        unsubscribed = three_users[2]['value']
        self.assertEqual(actives, 1)
        self.assertEqual(on_holiday, 1)
        self.assertEqual(unsubscribed, 1)



class Global_Job_Categories_TestCase(TestCase):

    def test_job_categories_json(self):
        """
        VISIT_AT_HOME = '1'
        ACCOMPANY_SOMEONE = '2'
        TRANSPORT_BY_CAR = '3'
        SHOPPING = '4'
        HOUSEHOULD = '5'
        HANDYMAN_JOBS = '6'
        GARDENING_JOBS = '7'
        PETS_CARE = '8'
        PERSONAL_CARE = '9'
        ADMINISTRATION = 'a'
        OTHER = 'b'
        """

        # Empty test
        empty = json.loads(get_job_categories_json())
        data  = empty['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # Create users
        creator = User.objects.create(username='creator_user')
        donor   = User.objects.create(username='donor')
        branch  = Branch.objects.create(creator=creator, name='my_branch')

        # Test job categories

        Demand.objects.create(branch=branch, category=[JobCategory.VISIT_AT_HOME], donor=donor, date=timezone.now())
        visit_at_home = json.loads(get_job_categories_json())
        data = visit_at_home['datasets'][0]['data']
        self.assertEqual(data, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.ACCOMPANY_SOMEONE], donor=donor, date=timezone.now())
        accompany_someone = json.loads(get_job_categories_json())
        data = accompany_someone['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.TRANSPORT_BY_CAR], donor=donor, date=timezone.now())
        transport_by_car = json.loads(get_job_categories_json())
        data = transport_by_car['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.SHOPPING], donor=donor, date=timezone.now())
        shopping = json.loads(get_job_categories_json())
        data = shopping['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.HOUSEHOULD], donor=donor, date=timezone.now())
        household = json.loads(get_job_categories_json())
        data = household['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.HANDYMAN_JOBS], donor=donor, date=timezone.now())
        handyman_jobs = json.loads(get_job_categories_json())
        data = handyman_jobs['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.GARDENING_JOBS], donor=donor, date=timezone.now())
        gardening_jobs = json.loads(get_job_categories_json())
        data = gardening_jobs['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.PETS_CARE], donor=donor, date=timezone.now())
        pets_care = json.loads(get_job_categories_json())
        data = pets_care['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.PERSONAL_CARE], donor=donor, date=timezone.now())
        personal_care = json.loads(get_job_categories_json())
        data = personal_care['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.ADMINISTRATION], donor=donor, date=timezone.now())
        administration = json.loads(get_job_categories_json())
        data = administration['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0])

        Demand.objects.create(branch=branch, category=[JobCategory.OTHER], donor=donor, date=timezone.now())
        other = json.loads(get_job_categories_json())
        data = other['datasets'][0]['data']
        self.assertEqual(data, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])



class User_Job_Categories_Statistics(TestCase):

    def test_user_job_categories_json(self):
        """
        Test job categories of user
        """

        # Create users
        donor_id = 5
        creator = User.objects.create(username='creator_user')
        donor   = User.objects.create(id=donor_id, username='donor')
        branch  = Branch.objects.create(creator=creator, name='my_branch')

        # Test empty jobs
        empty = json.loads(get_user_job_categories_json(donor_id))
        data = empty['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # Test that one job has been added
        Demand.objects.create(branch=branch, category=['1'], donor=donor, date=timezone.now())
        one_job = json.loads(get_user_job_categories_json(donor_id))
        data = one_job['datasets'][0]['data']
        self.assertEqual(data, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])



class User_Job_Avg_Time_Statistics(TestCase):

    def test_user_job_avg_time_json(self):
        """
        Test job average time of user
        """

        # Create users
        donor_id = 5
        creator = User.objects.create(username='creator_user')
        donor   = User.objects.create(id=donor_id, username='donor')
        branch  = Branch.objects.create(creator=creator, name='my_branch')

        # Test empty jobs
        empty = json.loads(get_user_job_avg_time_json(donor_id))
        data = empty['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # Test that one job has been added
        Demand.objects.create(branch=branch, category=['1'], donor=donor, real_time=30, date=timezone.now())
        one_job = json.loads(get_user_job_avg_time_json(donor_id))
        data = one_job['datasets'][0]['data']
        self.assertEqual(data, [30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # Test that a second job has been added
        Demand.objects.create(branch=branch, category=['1'], donor=donor, real_time=50, date=timezone.now())
        one_job = json.loads(get_user_job_avg_time_json(donor_id))
        data = one_job['datasets'][0]['data']
        self.assertEqual(data, [40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])




class User_Jobs_Amount_Statistics(TestCase):

    def test_user_jobs_amount_json(self):
        """
        Test job amount of user in the last 6 months
        """

        # Create users
        donor_id = 5
        creator = User.objects.create(username='creator_user')
        donor   = User.objects.create(id=donor_id, username='donor')
        branch  = Branch.objects.create(creator=creator, name='my_branch')

        # Test empty jobs
        empty = json.loads(get_user_jobs_amount_json(donor_id))
        data = empty['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0])

        # Test that one job has been added
        Demand.objects.create(branch=branch, category=[JobCategory.OTHER], donor=donor, date=timezone.now())
        one_job = json.loads(get_user_jobs_amount_json(donor_id))
        data = one_job['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 1])




class User_Time_Amount_Statistics(TestCase):

    def test_user_time_amount_json(self):
        """
        Test time taken by user for jobs in the last 6 months
        """

        # Create users
        donor_id = 5
        creator = User.objects.create(username='creator_user')
        donor   = User.objects.create(id=donor_id, username='donor')
        branch  = Branch.objects.create(creator=creator, name='my_branch')

        # Test empty jobs
        empty = json.loads(get_user_time_amount_json(donor_id))
        data = empty['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0])

        # Test that one job has been added
        Demand.objects.create(branch=branch, category=[JobCategory.OTHER], donor=donor, real_time=50, date=timezone.now())
        one_job = json.loads(get_user_time_amount_json(donor_id))
        data = one_job['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 50])



class User_Km_Amount_Statistics(TestCase):

    def test_user_km_amount_json(self):
        """
        Test kilometers covered by user for jobs in the last 6 months
        """

        # Create users
        donor_id = 5
        creator = User.objects.create(username='creator_user')
        donor   = User.objects.create(id=donor_id, username='donor')
        branch  = Branch.objects.create(creator=creator, name='my_branch')

        # Test empty jobs
        empty = json.loads(get_user_km_amount_json(donor_id))
        data = empty['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 0])

        # Test that one job has been added
        Demand.objects.create(branch=branch, category=[JobCategory.OTHER], donor=donor, km=50, date=timezone.now())
        one_job = json.loads(get_user_km_amount_json(donor_id))
        data = one_job['datasets'][0]['data']
        self.assertEqual(data, [0, 0, 0, 0, 0, 50])




class StatisticsTestCase(TestCase):

    def test_month_list(self):
        # month_list(i, n) return a month 'number' from i to n-1
        ls_month = month_list(1, 7)
        expected = [1, 2, 3, 4, 5, 6]
        self.assertEqual(ls_month, expected)

        ls_month = month_list(10, 4)
        expected = [10, 11, 12, 1, 2, 3]
        self.assertEqual(ls_month, expected)


    def test_previous_month(self):
        self.assertEqual(previous_month(10), 9)
        self.assertEqual(previous_month(1), 12)


    def test_next_month(self):
        self.assertEqual(next_month(8), 9)
        self.assertEqual(next_month(12), 1)


    def test_days_in_month(self):
        self.assertEqual(get_days_in_month(1), 31)
        self.assertEqual(get_days_in_month(2), 28)
        self.assertEqual(get_days_in_month(3), 31)
        self.assertEqual(get_days_in_month(4), 30)
        self.assertEqual(get_days_in_month(5), 31)
        self.assertEqual(get_days_in_month(6), 30)
        self.assertEqual(get_days_in_month(7), 31)
        self.assertEqual(get_days_in_month(8), 31)
        self.assertEqual(get_days_in_month(9), 30)
        self.assertEqual(get_days_in_month(10), 31)
        self.assertEqual(get_days_in_month(11), 30)
        self.assertEqual(get_days_in_month(12), 31)

