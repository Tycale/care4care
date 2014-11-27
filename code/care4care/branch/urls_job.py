from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView

from branch.views import NeedHelpView, OfferHelpView
from branch.forms import NeedHelpForm

urlpatterns = patterns('',
                       url(r'^needhelp/$',
                           NeedHelpView.as_view(),
                           name='need_help'),
                       url(r'^offerhelp/$',
                            NeedHelpView.as_view(),
                           name='offer_help'),
                       )
