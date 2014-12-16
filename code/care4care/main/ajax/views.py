from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from branch.models import Demand, Job, BranchMembers
from main.models import *
from django.utils import timezone
from django.db.models import Count, Avg, Sum
import json
from django.db import connection


MONTHS = {
    1:  {'name': _("Janvier"),     'days': 31},
    2:  {'name': _("Février"),     'days': 28},
    3:  {'name': _("Mars"),        'days': 31},
    4:  {'name': _("Avril"),       'days': 30},
    5:  {'name': _("Mai"),         'days': 31},
    6:  {'name': _("Juin"),        'days': 30},
    7:  {'name': _("Juillet"),     'days': 31},
    8:  {'name': _("Août"),        'days': 31},
    9:  {'name': _("Septembre"),   'days': 30},
    10: {'name': _("Octobre"),     'days': 31},
    11: {'name': _("Novembre"),    'days': 30},
    12: {'name': _("Décembre"),    'days': 31}
}


def previous_month(n):
    if n == 1:
        return len(MONTHS)
    else:
        return n-1


def next_month(n):
    n = n % len(MONTHS)
    return n+1


def month_list(i, n):
    result = []
    while i != n:
        result.append(i)
        i = next_month(i)
    return result


def get_last_n_months(n):
    now = timezone.now()
    last_m = []
    this_month = now.month
    i = now.month
    for j in range(1, n):
        i = previous_month(i)

    nex_month = next_month(this_month)
    while i != nex_month:
        last_m.append(str(MONTHS[i]['name']))
        i = next_month(i)
    return last_m


def get_days_in_month(n):
    return MONTHS[n]['days']


def get_last_day_of_month(month_date):
    n = month_date.month
    days_of_month_n = get_days_in_month(n)
    n_months_ago = month_date.replace(day=days_of_month_n, hour=23, minute=59, second=59, microsecond=0)
    return n_months_ago


def get_job_labels():
    return [str(l[1]) for l in JobCategory.JOB_CATEGORIES]



class Color:
    """
    Colors RGB - used for the stats json
    """
    LIGHT_BLUE_RGB = [151, 187, 205]
    LIGHT_BLUE_HEX = '#97BBCD'
    GREEN_RGB  = [46, 217, 138]
    GREEN_HEX  = '#2ED98A'
    ORANGE_RGB = [255, 169, 0]
    ORANGE_HEX = '#FFA900'
    RED_HEX = '#F7464A'


    
    def rgba(my_rgb, a):
        rgb_values = ','.join(map(str, my_rgb))
        return 'rgba('+rgb_values+', '+str(a)+')'




### Statistics

# Account status colors
ACTIVE_COLOR_HEX = Color.GREEN_HEX
ON_HOLIDAY_COLOR_HEX = Color.LIGHT_BLUE_HEX
UNSUBSCRIBED_COLOR_HEX = Color.ORANGE_HEX

# Account types colors
MEMBER_COLOR_HEX = Color.ORANGE_HEX
VERIFIED_MEMBER_COLOR_HEX = Color.GREEN_HEX
NON_MEMBER_COLOR_HEX = Color.LIGHT_BLUE_HEX



def generate_line_colors(color_rgb):
    return {
        'fillColor': Color.rgba(color_rgb, 0.2),
        'strokeColor': Color.rgba(color_rgb, 1),
        'pointColor': Color.rgba(color_rgb, 1),
        'pointStrokeColor': "#fff",
        'pointHighlightFill': "#fff",
        'pointHighlightStroke': Color.rgba(color_rgb, 1),
    }



# Global statistics


def get_users_registrated_json():
    response = {}

    N_MONTHS = 7

    response['labels'] = get_last_n_months(N_MONTHS)
    line_data = generate_line_colors(Color.LIGHT_BLUE_RGB)
    #line_data['data'] = [10, 15, 22, 33, 48, 69, 99]
    values = []
    now = timezone.now()
    for i in range(-N_MONTHS+1, 1):
        i_weeks_ago = now + timezone.timedelta(weeks=4*i)
        i_months_ago = get_last_day_of_month(i_weeks_ago)
        #print(-i, 'months_ago =>', i_months_ago)   # The Mayas watcher
        users_im = User.objects.filter(date_joined__lte=i_months_ago).count()
        values.append(users_im)
    line_data['data'] = values

    response['datasets'] = [line_data]
    return json.dumps(response)



def get_account_types_json():
    members = {}
    members['label'] = __('Membres')
    #members['value'] = 69
    members['value'] = User.objects.filter(user_type=MemberType.MEMBER).count()
    members['color'] = MEMBER_COLOR_HEX

    verif_members = {}
    verif_members['label'] = __('Membres vérifiés')
    #verif_members['value'] = 21
    verif_members['value'] = User.objects.filter(user_type=MemberType.VERIFIED_MEMBER).count()
    verif_members['color'] = VERIFIED_MEMBER_COLOR_HEX

    non_members = {}
    non_members['label'] = __('Non-membres')
    #non_members['value'] = 10
    non_members['value'] = User.objects.filter(user_type=MemberType.NON_MEMBER).count()
    non_members['color'] = NON_MEMBER_COLOR_HEX

    response = [members, verif_members, non_members]

    return json.dumps(response)



def get_users_status_json():
    actives = {}
    actives['label'] = __('Actifs')
    #actives['value'] = 80
    actives['value'] = User.objects.filter(status=STATUS[ACTIVE-1][0]).count()
    actives['color'] = ACTIVE_COLOR_HEX

    on_holiday = {}
    on_holiday['label'] = __('En vacances')
    #on_holiday['value'] = 18
    on_holiday['value'] = User.objects.filter(status=STATUS[HOLIDAYS-1][0]).count()
    on_holiday['color'] = ON_HOLIDAY_COLOR_HEX

    unsubscribed = {}
    unsubscribed['label'] = __('Désactivés')
    #unsubscribed['value'] = 2
    unsubscribed['value'] = User.objects.filter(status=STATUS[UNSUBSCRIBE-1][0]).count()
    unsubscribed['color'] = UNSUBSCRIBED_COLOR_HEX

    response = [actives, on_holiday, unsubscribed]
    return json.dumps(response)


def get_job_categories_json():
    response = {}
    response['labels'] = get_job_labels()
    datasets = []
    first_dataset = generate_line_colors(Color.LIGHT_BLUE_RGB)
    #first_dataset['label'] = __('Jobs effectués par catégorie')  # Non-necessary field
    #first_dataset['data'] = [40, 30, 60, 70, 25, 47, 39, 69, 34, 23, 31, 69]
    values = []
    for job in JobCategory.JOB_CATEGORIES:
        values.append(Demand.objects.filter(category__in=job[0]).exclude(donor=None).count())
    first_dataset['data'] = values

    datasets.append(first_dataset)

    response['datasets'] = datasets
    return json.dumps(response)



# Branch statistics

def get_branch_users_registrated_json(branch_id):
    users_id = BranchMembers.objects.filter(branch__id=branch_id).values_list('user', flat=True)
    users = User.objects.filter(id__in=users_id)
    response = {}

    N_MONTHS = 7

    response['labels'] = get_last_n_months(N_MONTHS)
    line_data = generate_line_colors(Color.LIGHT_BLUE_RGB)
    #line_data['data'] = [10, 15, 22, 33, 48, 69, 99]
    values = []
    now = timezone.now()
    for i in range(-N_MONTHS+1, 1):
        i_weeks_ago = now + timezone.timedelta(weeks=4*i)
        i_months_ago = get_last_day_of_month(i_weeks_ago)
        #print(-i, 'months_ago =>', i_months_ago)   # The Mayas watcher
        users_im = users.filter(date_joined__lte=i_months_ago).count()
        values.append(users_im)
    line_data['data'] = values

    response['datasets'] = [line_data]
    return json.dumps(response)


def get_branch_account_types_json(branch_id):
    users_id = BranchMembers.objects.filter(branch__id=branch_id).values_list('user', flat=True)

    members = {}
    members['label'] = __('Membres')
    #members['value'] = 69
    members['value'] = User.objects.filter(id__in=users_id, user_type=MemberType.MEMBER).count()
    members['color'] = MEMBER_COLOR_HEX

    verif_members = {}
    verif_members['label'] = __('Membres vérifiés')
    #verif_members['value'] = 21
    verif_members['value'] = User.objects.filter(id__in=users_id, user_type=MemberType.VERIFIED_MEMBER).count()
    verif_members['color'] = VERIFIED_MEMBER_COLOR_HEX

    non_members = {}
    non_members['label'] = __('Non-membres')
    #non_members['value'] = 10
    non_members['value'] = User.objects.filter(id__in=users_id, user_type=MemberType.NON_MEMBER).count()
    non_members['color'] = NON_MEMBER_COLOR_HEX

    response = [members, verif_members, non_members]

    return json.dumps(response)


def get_branch_user_status_json(branch_id):
    users_id = BranchMembers.objects.filter(branch__id=branch_id).values_list('user', flat=True)

    actives = {}
    actives['label'] = __('Actifs')
    #actives['value'] = 80
    actives['value'] = User.objects.filter(id__in=users_id, status=STATUS[ACTIVE-1][0]).count()
    actives['color'] = ACTIVE_COLOR_HEX

    on_holiday = {}
    on_holiday['label'] = __('En vacances')
    #on_holiday['value'] = 18
    on_holiday['value'] = User.objects.filter(id__in=users_id, status=STATUS[HOLIDAYS-1][0]).count()
    on_holiday['color'] = ON_HOLIDAY_COLOR_HEX

    unsubscribed = {}
    unsubscribed['label'] = __('Désactivés')
    #unsubscribed['value'] = 2
    unsubscribed['value'] = User.objects.filter(id__in=users_id, status=STATUS[UNSUBSCRIBE-1][0]).count()
    unsubscribed['color'] = UNSUBSCRIBED_COLOR_HEX

    response = [actives, on_holiday, unsubscribed]
    return json.dumps(response)


def get_branch_job_categories_json(branch_id):
    users_id = BranchMembers.objects.filter(branch__id=branch_id).values_list('user', flat=True)

    response = {}
    response['labels'] = get_job_labels()
    datasets = []
    first_dataset = generate_line_colors(Color.LIGHT_BLUE_RGB)
    #first_dataset['label'] = __('Jobs effectués par catégorie')  # Non-necessary field
    #first_dataset['data'] = [40, 30, 60, 70, 25, 47, 39, 69, 34, 23, 31, 69]
    values = []
    for job in JobCategory.JOB_CATEGORIES:
        values.append(Demand.objects.filter(donor__in=users_id, category__in=str(job[0]),branch__id=branch_id).count())
    first_dataset['data'] = values

    datasets.append(first_dataset)

    response['datasets'] = datasets
    return json.dumps(response)






# User statistics


def get_user_job_categories_json(user_id):
    response = {}
    response['labels'] = get_job_labels()
    datasets = []
    first_dataset = generate_line_colors(Color.GREEN_RGB)
    #first_dataset['label'] = __('Membres')  # Non-necessary field
    # get user
    user = User.objects.get(pk=user_id)
    # group by django
    nb_demands = Demand.objects.filter(donor=user).values('category').annotate(number=Count('category'))
    # construct data list
    data_list = [0 for i in range(0, len(JobCategory.JOB_CATEGORIES))]
    for d in nb_demands:
        for (i, job_cat) in enumerate(JobCategory.JOB_CATEGORIES):
            if d['category'] == str(job_cat[0]):
                data_list[i] += 1

    first_dataset['data'] = data_list
    datasets.append(first_dataset)
    response['datasets'] = datasets
    return json.dumps(response)



def get_user_job_avg_time_json(user_id):
    response = {}
    response['labels'] = get_job_labels()
    datasets = []
    first_dataset = generate_line_colors(Color.GREEN_RGB)

    user = User.objects.get(pk=user_id)
    #group by django
    nb_demands = Demand.objects.filter(donor=user).values('category').annotate(help_time=Avg('real_time'))
    #construct data list
    data_list = [{'number':0, 'total_time':0} for i in range(0, len(JobCategory.JOB_CATEGORIES))]
    for d in nb_demands:
        for (i, job_cat) in enumerate(JobCategory.JOB_CATEGORIES):
            if d['category'] == job_cat[0] and d['help_time'] is not None:
                data_list[i]['total_time'] += d['help_time']
                data_list[i]['number'] += 1

    # Compute average
    data_avg = []
    for data in data_list:
        total_time = data['total_time']
        number = data['number']
        d_avg  = 0.0
        if number != 0:
            d_avg = total_time // number    # integer division
        data_avg.append(d_avg)

    first_dataset['data'] = data_avg
    datasets.append(first_dataset)

    response['datasets'] = datasets
    return json.dumps(response)




def get_user_jobs_amount_json(user_id):
    response = {}

    N_MONTHS = 6
    response['labels'] = get_last_n_months(N_MONTHS)

    truncate_date = connection.ops.date_trunc_sql('month', 'date')
    now = timezone.now()
    this_month = get_last_day_of_month(now)
    # get date minus 6 months (in number of weeks actually)
    i_months_ago = this_month - timezone.timedelta(weeks=4*N_MONTHS)
    # set the last day of that month
    i_months_ago = get_last_day_of_month(i_months_ago)
    user = User.objects.get(pk=user_id)
    jobs_amount = Demand.objects.filter(donor=user, date__gte=i_months_ago, date__lte=now)
    # data_list contains the number of the months
    data_list = month_list(i_months_ago.month, next_month(this_month.month))
    data_dict = dict.fromkeys(data_list, 0)

    for job in jobs_amount:
        data_dict[job.date.month] += 1

    # Copy data from dictionary
    for (i, month_num) in enumerate(data_list):
        data_list[i] = data_dict[month_num]

    datasets = []
    first_dataset = generate_line_colors(Color.LIGHT_BLUE_RGB)
    #first_dataset['label'] = __('Membres')  # Non-necessary field
    first_dataset['data'] = data_list
    datasets.append(first_dataset)

    response['datasets'] = datasets
    return json.dumps(response)




def get_user_time_amount_json(user_id):
    response = {}

    N_MONTHS = 6

    response['labels'] = get_last_n_months(N_MONTHS)

    truncate_date = connection.ops.date_trunc_sql('month', 'date')
    now = timezone.now()
    this_month = get_last_day_of_month(now)
    # get date minus 6 months (in number of weeks actually)
    i_months_ago = this_month - timezone.timedelta(weeks=4*N_MONTHS)
    # set the last day of that month
    i_months_ago = get_last_day_of_month(i_months_ago)
    user = User.objects.get(pk=user_id)
    jobs_amount = Demand.objects.filter(donor=user, date__gte=i_months_ago, date__lte=now).extra({'month': truncate_date}).values('month').annotate(created_count=Sum('real_time'))
    data_list = [0 for i in range(0, N_MONTHS)]
    baseIndex = i_months_ago.month
    # the base index is the first month and is equal to the index 0 in the data_list
    # the key is the month number
    for job in jobs_amount:
        key = int(job['month'].month)
        if job['created_count'] is not None:
            data_list[key - baseIndex] = job['created_count']

    datasets = []
    first_dataset = generate_line_colors(Color.LIGHT_BLUE_RGB)
    #first_dataset['label'] = __('Membres')  # Non-necessary field
    #first_dataset['data'] = [10, 20, 30, 42, 25, 28]
    first_dataset['data'] = data_list
    datasets.append(first_dataset)

    response['datasets'] = datasets
    return json.dumps(response)



def get_user_km_amount_json(user_id):
    response = {}

    N_MONTHS = 6

    response['labels'] = get_last_n_months(N_MONTHS)

    truncate_date = connection.ops.date_trunc_sql('month', 'date')
    now = timezone.now()
    this_month = get_last_day_of_month(now)
    # get date minus 6 months (in number of weeks actually)
    n_months_ago = this_month - timezone.timedelta(weeks=4*N_MONTHS)
    # set the last day of that month
    n_months_ago = get_last_day_of_month(n_months_ago)
    user = User.objects.get(pk=user_id)
    jobs_amount = Demand.objects.filter(donor=user, date__gte=n_months_ago, date__lte=now).extra({'month': truncate_date}).values('month').annotate(km_amount=Sum('km'))
    data_list = [0 for i in range(0, N_MONTHS)]
    baseIndex = n_months_ago.month
    # the base index is the first month and is equal to the index 0 in the data_list
    # the key is the month number
    for job in jobs_amount:
        #print('job', job)
        key = int(job['month'].month)
        km_amount = job['km_amount']
        if km_amount is not None:
            data_list[key - baseIndex] = km_amount

    datasets = []
    first_dataset = generate_line_colors(Color.LIGHT_BLUE_RGB)
    #first_dataset['label'] = __('Membres')  # Non-necessary field
    #first_dataset['data'] = [10, 20, 30, 42, 25, 28]
    first_dataset['data'] = data_list
    datasets.append(first_dataset)

    response['datasets'] = datasets
    return json.dumps(response)

