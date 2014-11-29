from django.conf.urls import patterns, url
from main.views import statistics, get_registrated_users_json


urlpatterns = patterns(
	'',
	url(r'^$', statistics, name='stats'),
	url(r'^registrated_users_json$', get_registrated_users_json, name='stats_reg_users_json'),
)