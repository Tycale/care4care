#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('news.views',
	url(r'^(?P<slug>[-\w\d]+)-(?P<id>\d+)\.html$', 'read', name='news_read'),
	url(r'^add/$', 'add', name='news_add'),
	url(r'^modify/(?P<id>\d+),(?P<slug>[-\w\d]+)/$', 'modify', name='news_modify'),
	url(r'^$', 'list', name='news_home'),
)