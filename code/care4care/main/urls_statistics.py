from django.conf.urls import patterns, url
from main.views import statistics, get_registrated_users_json, get_account_types_json,\
                        get_users_status_json, get_job_categories_json, \
                        get_user_job_categories_json, get_user_job_avg_time_json, \
                        get_user_jobs_amount_json, get_user_time_amount_json, get_user_km_amount_json, \
                        get_registrated_users_json_branch, get_job_categories_json_branch


urlpatterns = patterns(
    '',
    # Global statistics
    url(r'^$', statistics, name='stats'),
    url(r'^registrated_users_json/(?P<branch_id>\d+)/$', get_registrated_users_json_branch, name='branch_stats_reg_users_json'),
    url(r'^job_categories_json/(?P<branch_id>\d+)/$', get_job_categories_json_branch, name='branch_stats_job_categories_json'),

    url(r'^registrated_users_json$', get_registrated_users_json, name='stats_reg_users_json'),
    url(r'^account_types_json$', get_account_types_json, name='stats_account_types_json'),
    url(r'^users_status_json$', get_users_status_json, name='stats_users_status_json'),
    url(r'^job_categories_json$', get_job_categories_json, name='stats_job_categories_json'),

    # User statistics
    url(r'^user_job_categories_json/(?P<user_id>\d+)/$',
        get_user_job_categories_json,
        name='user_stats_job_categories_json'),
    url(r'^user_job_avg_time_json/(?P<user_id>\d+)/$',
        get_user_job_avg_time_json,
        name='user_stats_job_avg_time_json'),
    url(r'^user_jobs_amount_json/(?P<user_id>\d+)/$',
        get_user_jobs_amount_json,
        name='user_jobs_amount_json'),
    url(r'^user_time_amount_json/(?P<user_id>\d+)/$',
        get_user_time_amount_json,
        name='user_stats_time_amount_json'),
    url(r'^user_km_amount_json/(?P<user_id>\d+)/$',
        get_user_km_amount_json,
        name='user_stats_km_amount_json'),
)
