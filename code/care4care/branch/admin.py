from django.contrib import admin

from branch.models import Demand, Offer, Comment

class OfferAdmin(admin.ModelAdmin):
    pass

class DemandAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Demand, DemandAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Comment, CommentAdmin)
