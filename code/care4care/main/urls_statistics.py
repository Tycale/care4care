from django.conf.urls import patterns, url
from main.views import statistics, get_registrated_users_json, get_account_types_json,\
                        get_users_status_json, get_job_categories_json


urlpatterns = patterns(
    '',
    url(r'^$', statistics, name='stats'),
    url(r'^registrated_users_json$', get_registrated_users_json, name='stats_reg_users_json'),
    url(r'^account_types_json$', get_account_types_json, name='stats_account_types_json'),
    url(r'^users_status_json$', get_users_status_json, name='stats_users_status_json'),
    url(r'^job_categories_json$', get_job_categories_json, name='stats_job_categories_json'),
)
