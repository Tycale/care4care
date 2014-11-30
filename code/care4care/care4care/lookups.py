from ajax_select import LookupChannel

from main.models import User

class UserLookup(LookupChannel):

    model = User

    def get_query(self, q, request):
        return User.objects.filter(username__icontains=q)

    def get_result(self, obj):
        return obj.username

    def check_auth(self, request):
    	return request.user.is_authenticated()

