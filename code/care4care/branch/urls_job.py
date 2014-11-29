from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView

from branch.views import NeedHelpView, OfferHelpView, DetailJobView

urlpatterns = patterns('',
                       url(r'^needhelp/(?P<user_id>\d+)/$',
                           NeedHelpView.as_view(),
                           name='need_help'),
                       url(r'^offerhelp/(?P<user_id>\d+)/$',
                            OfferHelpView.as_view(),
                           name='offer_help'),
                       url(r'^details/(?P<job_id>\d+)/$',
                            DetailJobView.as_view(),
                           name='see_help'),
                       )
