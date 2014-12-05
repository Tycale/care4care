#-*- coding: utf-8 -*-
from news.models import News
from news.forms import NewsForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.utils import timezone

def read(request, id, slug):
    """ View for displaying a signle news """
    a = get_object_or_404(News, id=id)

    return render(request, 'read.html', locals())

def add(request):
    """ View  for creating a news """
    if request.method == "POST":
        form = NewsForm(request.user, request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                art = form.save(commit=False)
                art.nom_auteur = request.user.username
                art.auteur = request.user
                art.visible = True
                art.date_debut = timezone.now()
                art.save()


            messages.success(request, _("Votre news a été créee."))
            return redirect('news_home')
        else:
            messages.error(request, _("Un problème s'est déroulé lors de la création de la news."))
    else:
        if not request.user.is_superuser:
            messages.info(request, u("Vous devez être super utilisateur pour écrire une news"))
        form = NewsForm(request.user)
    return render(request, 'add.html', locals())

def list(request, slug='all', page=1):
    """ View used for displaying the list on the latest news """
    news = News.objects.filter(visible=True)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(news, 5)
    try:
        news = paginator.page(page)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'news.html', locals())

def modify(request, id, slug):
    """ View  for creating a news """
    article = get_object_or_404(News, id=id)
    modify = True
    if  not request.user.is_superuser:
        messages.error(request, _("Vous n\'avez pas pas le droit de modifier cette news."))
        return redirect('home')

    if request.method == "POST":
        form = NewsForm(request.user, request.POST, instance=article)
        if form.is_valid():
            auteur = article.auteur
            form.auteur = auteur
            v = form.save(commit=False)
            v.date_creation = datetime.now()
            v.save()
            messages.success(request, _("Votre news a été modifiée."))

            return redirect('news_home')
        else:
            messages.error(request, _("Un problème s'est déroulé lors de la modification de la news."))
    else:
        form = NewsForm(request.user, instance=article)
    return render(request, 'add.html', locals())

