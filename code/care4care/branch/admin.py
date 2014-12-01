from django.contrib import admin

from branch.models import Demand, Offer, Comment, Branch

class OfferAdmin(admin.ModelAdmin):
    list_display = ('category', 'get_user', 'branch', 'date',)
    search_fields = ('get_user','branch','category','title')
    def get_user(self, obj):
        return obj.offer.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'

class DemandAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'get_user', 'branch', 'date',)
    search_fields = ('get_user','branch','category','title')
    def get_user(self, obj):
        return obj.receiver.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'

class CommentAdmin(admin.ModelAdmin):
    pass

class BranchAdmin(admin.ModelAdmin):
    pass

admin.site.register(Demand, DemandAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Branch, BranchAdmin)

