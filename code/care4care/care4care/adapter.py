from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import (get_user_model, serialize_instance,
deserialize_instance)
from main.models import User

class MyAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        sociallogin.account.user.is_active = True
        if sociallogin.account.provider == "twitter":
            username = data['name']
        else:
            username = data['first_name'] + data['last_name']
            sociallogin.account.user.first_name = data.get('first_name')
            sociallogin.account.user.last_name = data.get('last_name')
            sociallogin.account.user.email = data.get('email')
            sociallogin.account.user.name = data.get('name')

        if User.objects.filter(username=username).exists():
            base_username = username
            count = 1
            while User.objects.filter(username=username).exists():
                username = base_username + str(count)
                count += 1


        data['username'] = username
        super(MyAccountAdapter,self).populate_user(request, sociallogin, data)
