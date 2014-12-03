from ajax_select import LookupChannel

from main.models import User
from django.db.models import Q

class UserLookup(LookupChannel):

    model = User

    def get_query(self, q, request):
        return User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))

    def get_result(self, obj):
        return obj.username

    def format_match(self,obj):
    	return '{} [{}]'.format(obj.get_full_name(), obj.username) 

    def check_auth(self, request):
    	return request.user.is_authenticated()
