from django.contrib import admin

from branch.models import Demand, Offer, Comment, Branch, DemandProposition, SuccessDemand

class OfferAdmin(admin.ModelAdmin):
    """ Display Offer Admin """
    list_display = ('get_verbose_category', 'get_user', 'branch', 'date',)
    search_fields = ('get_user','branch','category','title')
    def get_user(self, obj):
        return obj.donor.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'

class DemandAdmin(admin.ModelAdmin):
    """ Display Demand Admin """
    list_display = ('title','get_verbose_category', 'get_user', 'branch', 'date',)
    search_fields = ('get_user','branch','category','title')
    def get_user(self, obj):
        return obj.receiver.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'

class CommentAdmin(admin.ModelAdmin):
    pass

class BranchAdmin(admin.ModelAdmin):
    pass

class DemandPropositionAdmin(admin.ModelAdmin):
    pass

class SuccessDemandAdmin(admin.ModelAdmin):
    pass

admin.site.register(Demand, DemandAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(DemandProposition, DemandPropositionAdmin)
admin.site.register(SuccessDemand, SuccessDemandAdmin)
