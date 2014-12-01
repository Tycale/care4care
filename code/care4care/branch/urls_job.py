from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView

from branch.views import CreateDemandView, CreateOfferView, DetailDemandView, DetailOfferView, \
                          UpdateDemandView, UpdateOfferView, CreateVolunteerView

urlpatterns = patterns('',
                       url(r'^new/demand/(?P<user_id>\d+)/$',
                           CreateDemandView.as_view(),
                           name='create_demand'),
                       url(r'^update/demand/(?P<demand_id>\d+)/$',
                           UpdateDemandView.as_view(),
                           name='update_demand'),
                       url(r'^delete/demand/(?P<demand_id>\d+)/$',
                           'branch.views.delete_demand',
                           name='delete_demand'),
                       url(r'^delete/offer/(?P<offer_id>\d+)/$',
                           'branch.views.delete_offer',
                           name='delete_offer'),
                       url(r'^new/offer/(?P<user_id>\d+)/$',
                            CreateOfferView.as_view(),
                           name='create_offer'),
                       url(r'^update/offer/(?P<offer_id>\d+)/$',
                            UpdateOfferView.as_view(),
                           name='update_offer'),
                       url(r'^demand/(?P<demand_id>\d+)/$',
                            DetailDemandView.as_view(),
                           name='see_demand'),
                       url(r'^offer/(?P<offer_id>\d+)/$',
                            DetailOfferView.as_view(),
                           name='see_offer'),
                       # volunteer
                       url(r'^volunteer/(?P<volunteer_id>\d+)/demand/(?P<demand_id>\d+)/$',
                            CreateVolunteerView.as_view(),
                            name='volunteer_demand'),
                       )
