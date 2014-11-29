from django.conf.urls import patterns, url
from main.views import similar_jobs, similar_offers, similar_demands

urlpatterns = patterns('',
                       url(r'^$',
                            similar_jobs,
                            name='similar_jobs'),
                       url(r'^offers/$',
                            similar_offers,
                            name='similar_offers'),
                       url(r'^demands/$',
                            similar_demands,
                            name='similar_demands'),
                       )