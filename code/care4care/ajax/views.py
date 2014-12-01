from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from branch.models import Demand, Job
from main.models import User, MemberType, JobCategory
from django.utils import timezone
from django.db.models import Count, Avg
import datetime
import json
from django.db import connection


MONTHS = {
    1: __("Janvier"),
    2: __("Février"),
    3: __("Mars"),
    4: __("Avril"),
    5: __("Mai"),
    6: __("Juin"),
    7: __("Juillet"),
    8: __("Août"),
    9: __("Septembre"),
    10: __("Octobre"),
    11: __("Novembre"),
    12: __("Décembre")
}



class Color:
    """
    Colors RGB - used for the stats json
    """
    LIGHT_BLUE_RGB = [151, 187, 205]
    GREEN_RGB  = [46, 217, 138]
    ORANGE_RGB = [255, 169, 0]

    @staticmethod
    def rgba(my_rgb, a):
        rgb_values = ','.join(map(str, my_rgb))
        return 'rgba('+rgb_values+', '+str(a)+')'


class Statistics:
    """
    Statistics class
    """

    @staticmethod
    def generate_line_colors(color_rgb):
        return {
            'fillColor': Color.rgba(color_rgb, 0.2),
            'strokeColor': Color.rgba(color_rgb, 1),
            'pointColor': Color.rgba(color_rgb, 1),
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': Color.rgba(color_rgb, 1),
        }



    @staticmethod
    def get_last_n_months(n):
        last_m = [datetime.date.today() + datetime.timedelta(weeks=4*(-i)) for i in range(0, n)]
        return [MONTHS[d.month] for d in reversed(last_m)]


    # Global statistics

    @staticmethod
    def get_users_registrated_json():
        response = {}

        """
        response['labels'] = [
            __("Juin"),
            __("Juillet"),
            __("Août"),
            __("Septembre"),
            __("Octobre"),
            __("Novembre),
            __("Décembre)
        ]
        """

        N_MONTHS = 7

        response['labels'] = Statistics.get_last_n_months(N_MONTHS)
        line_data = Statistics.generate_line_colors(Color.LIGHT_BLUE_RGB)
        #line_data['data'] = [10, 15, 22, 33, 48, 69, 99]
        values = []
        now = timezone.now()
        # Does not correspond to real months, rather every 4 weeks
        for i in range(-N_MONTHS+2, 2):
            i_months_ago = now + timezone.timedelta(weeks=4*i)
            users_im = User.objects.filter(date_joined__lte=i_months_ago).count()
            values.append(users_im)
        line_data['data'] = values

        response['datasets'] = [line_data]
        return json.dumps(response)


    @staticmethod
    def get_account_types_json():
        members = {}
        members['label'] = __('Membres')
        #members['value'] = 69
        members['value'] = User.objects.filter(user_type=MemberType.MEMBER).count()
        members['color'] = '#F7464A'

        verif_members = {}
        verif_members['label'] = __('Membres vérifiés')
        #verif_members['value'] = 21
        verif_members['value'] = User.objects.filter(user_type=MemberType.VERIFIED_MEMBER).count()
        verif_members['color'] = '#FDB45C'

        non_members = {}
        non_members['label'] = __('Non-membres')
        #non_members['value'] = 10
        non_members['value'] = User.objects.filter(user_type=MemberType.NON_MEMBER).count()
        non_members['color'] = '#46BFBD'

        response = [members, verif_members, non_members]

        return json.dumps(response)


    @staticmethod
    def get_users_status_json():
        response = {}
        response['labels'] = [
            __("Avril"),
            __("Mai"),
            __("Juin"),
            __("Juillet"),
            __("Août"),
            __("Septembre"),
            __("Octobre"),
        ]
        line_active = Statistics.generate_line_colors(Color.LIGHT_BLUE_RGB)
        line_active['data'] = [10, 12, 15, 20, 31, 51, 87]

        line_holiday = Statistics.generate_line_colors(Color.GREEN_RGB)
        line_holiday['data'] = [0, 3, 6, 12, 15, 15, 9]

        line_deactivated = Statistics.generate_line_colors(Color.ORANGE_RGB)
        line_deactivated['data'] = [0, 0, 1, 1, 2, 3, 3]

        response['datasets'] = [line_active, line_holiday, line_deactivated]
        return json.dumps(response)


    @staticmethod
    def get_job_categories_json():
        response = {}
        """response['labels'] = [
            __("Visites à domicile"),
            __("Tenir compagnie"),
            __("Transport par voiture"),
            __("Shopping"),
            __("Garder la maison"),
            __("Boulots manuels"),
            __("Jardinage"),
            __("Garder des animaux),
            __("Soins personnels"),
            __("Administratif"),
            __("Autre"),
            __("Spécial... :D"),
        ]"""
        response['labels'] = [str(l[1]) for l in JobCategory.JOB_CATEGORIES]
        datasets = []
        first_dataset = Statistics.generate_line_colors(Color.LIGHT_BLUE_RGB)
        #first_dataset['label'] = __('Jobs effectués par catégorie')  # Non-necessary field
        #first_dataset['data'] = [40, 30, 60, 70, 25, 47, 39, 69, 34, 23, 31, 69]
        print('wtf is this shit')
        values = []
        for l in JobCategory.JOB_CATEGORIES:
            print(l)
            print(str(l[0]))
            print(Demand.objects.all())
            print(Demand.objects.filter(category__in=str(l[0])))
            values.append(Demand.objects.filter(category__in=str(l[0])).count())
        print("values =", values)
        if len(values) == 0:
            print('wtf')
        first_dataset['data'] = values

        datasets.append(first_dataset)

        response['datasets'] = datasets
        return json.dumps(response)


    # User statistics

    @staticmethod
    def get_user_job_categories_json(user_id):
        print("get_user_job_categories_json")
        response = {}
        response['labels'] = [
            __("Visites à domicile"),
            __("Tenir compagnie"),
            __("Transport par voiture"),
            __("Shopping"),
            __("Garder la maison"),
            __("Boulots manuels"),
            __("Jardinage"),
            __("Soins personnels"),
            __("Administratif"),
            __("Autre"),
            __("Spécial... :D"),
        ]
        datasets = []
        first_dataset = Statistics.generate_line_colors(Color.GREEN_RGB)
        #first_dataset['label'] = __('Membres')  # Non-necessary field
        #get user
        user = User.objects.get(pk=user_id);
        #group by django
        nb_demands = Demand.objects.filter(receiver=user).values('category').annotate(number=Count('category'));
        #construct data list
        data_list = []
        for cat in JobCategory.JOB_CATEGORIES:
            data_list.append(0)
        for d in nb_demands:
            index = int(d["category"])
            data_list[index-1] = d["number"]

        first_dataset['data'] = data_list
        datasets.append(first_dataset)
        response['datasets'] = datasets
        return json.dumps(response)


    @staticmethod
    def get_user_job_avg_time_json(user_id):
        response = {}
        response['labels'] = [
            __("Visites à domicile"),
            __("Tenir compagnie"),
            __("Transport par voiture"),
            __("Shopping"),
            __("Garder la maison"),
            __("Boulots manuels"),
            __("Jardinage"),
            __("Soins personnels"),
            __("Administratif"),
            __("Autre"),
            __("Spécial... :D"),
        ]
        datasets = []
        first_dataset = Statistics.generate_line_colors(Color.GREEN_RGB)

        user = User.objects.get(pk=user_id);
        #group by django
        nb_demands = Demand.objects.filter(receiver=user).values('category').annotate(average_rating=Avg('estimated_time'));
        #construct data list
        data_list = []
        for cat in JobCategory.JOB_CATEGORIES:
            data_list.append(0)
        for d in nb_demands:
            index = int(d["category"])
            data_list[index-1] = d["average_rating"]

        first_dataset['data'] = data_list
        datasets.append(first_dataset)

        response['datasets'] = datasets
        return json.dumps(response)


    @staticmethod
    def get_user_km_json(user_id):
        response = {}

        N_MONTHS = 6

        response['labels'] = Statistics.get_last_n_months(N_MONTHS)

        #filter(pub_date__gte=timezone.now() + timezone.delta(months=-6))
        datasets = []
        first_dataset = Statistics.generate_line_colors(Color.LIGHT_BLUE_RGB)
        #first_dataset['label'] = __('Membres')  # Non-necessary field
        first_dataset['data'] = [10, 20, 30, 42, 25, 28]
        datasets.append(first_dataset)

        response['datasets'] = datasets
        return json.dumps(response)


    @staticmethod
    def get_user_jobs_amount_json(user_id):
        response = {}

        N_MONTHS = 6
        response['labels'] = Statistics.get_last_n_months(N_MONTHS)
        truncate_date = connection.ops.date_trunc_sql('month','date')
        jobs_amount = Demand.objects.extra({'month':truncate_date}).values('month').annotate(created_count=Count('id'))

        datasets = []
        first_dataset = Statistics.generate_line_colors(Color.LIGHT_BLUE_RGB)
        #first_dataset['label'] = __('Membres')  # Non-necessary field
        first_dataset['data'] = [10, 20, 30, 42, 25, 28]
        datasets.append(first_dataset)

        response['datasets'] = datasets
        return json.dumps(response)
