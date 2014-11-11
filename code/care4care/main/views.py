from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as _logout
from django.contrib.auth import authenticate, login as _login


# Create your views here.
def home(request):
    return render(request, 'main/home.html', locals())

def logout(request):
    _logout(request)
    messages.add_message(request, messages.INFO, _('Vous êtes désormais déconnecté.'))
    return redirect('home')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            _login(request, user)
            messages.add_message(request, messages.INFO, _('Vous êtes désormais connecté.'))
        else:
            messages.add_message(request, messages.ERROR, _('Impossible de vous connecter, vous \
                êtes innactif. Vérifiez vos emails afin de valider votre compte.'))
    else:
        messages.add_message(request, messages.ERROR, _('Impossible de se connecter.'))

    return redirect('home')
