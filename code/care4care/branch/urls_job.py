from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView

from branch.views import CreateDemandView, CreateOfferView, DetailDemandView, DetailOfferView

urlpatterns = patterns('',
                       url(r'^new/demand/(?P<user_id>\d+)/$',
                           CreateDemandView.as_view(),
                           name='create_demand'),
                       url(r'^new/offer/(?P<user_id>\d+)/$',
                            CreateOfferView.as_view(),
                           name='create_offer'),
                       url(r'^demand/(?P<demand_id>\d+)/$',
                            DetailDemandView.as_view(),
                           name='see_demand'),
                       url(r'^offer/(?P<offer_id>\d+)/$',
                            DetailOfferView.as_view(),
                           name='see_offer'),
                       )
