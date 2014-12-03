from django.contrib import admin
from news.models import News
# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_creation')
    list_filter = ('date_creation',)
admin.site.register(News, NewsAdmin)
