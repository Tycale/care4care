from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView,RedirectView

from postman import OPTIONS
from postman.views import (InboxView, SentView, ArchivesView, TrashView,
        WriteView, ReplyView, MessageView, ConversationView,
        ArchiveView, DeleteView, UndeleteView)

urlpatterns = patterns('postman.views',
    url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$',
        InboxView.as_view(template_name='messages/inbox.html'),
        name='postman_inbox'),
    url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', SentView.as_view(template_name='messages/sent.html'), name='postman_sent'),
    url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', ArchivesView.as_view(template_name='messages/archives.html'), name='postman_archives'),
    url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', TrashView.as_view(template_name='messages/trash.html'), name='postman_trash'),
    url(r'^write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(template_name='messages/write.html'), name='postman_write'),
    url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(template_name='messages/reply.html'), name='postman_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(template_name='messages/view.html'), name='postman_view'),
    url(r'^view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(template_name='messages/view.html'), name='postman_view_conversation'),
    url(r'^archive/$', ArchiveView.as_view(), name='postman_archive'),
    url(r'^delete/$', DeleteView.as_view(), name='postman_delete'),
    url(r'^undelete/$', UndeleteView.as_view(), name='postman_undelete'),
    (r'^$', RedirectView.as_view(url='inbox/')),
)
