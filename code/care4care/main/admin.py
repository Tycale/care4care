from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import User, VerifiedInformation, EmergencyContact

class CareUserAdmin(admin.ModelAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'is_staff')
    #list_filter = ('is_staff', 'is_superuser')
    #fieldsets = (
    #    (None, {'fields': ('email', 'password')}),
    #    ('Personal info', {'fields': ('first_name', 'last_name', 'credit', 
    #    	'birth_date', 'phone_number', 'mobile_number', 'location', 'latitude', 'longitude')}),
    #    ('Permissions', {'fields': ('is_verified', 'is_staff', 'is_superuser')}),
    #)
    ## add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    ## overrides get_fieldsets to use this attribute when creating a user.
    #add_fieldsets = (
    #    (None, {
    #        'classes': ('wide',),
    #        'fields': ('email', 'first_name', 'last_name', 'birth_date', 'password1', 'password2')}
    #    ),
    #)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    #ordering = ('email',)
    #filter_horizontal = ()
    #pass

class VerifiedInformationAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'recomendation_letter_1', 'recomendation_letter_2', 'criminal_record',)
    search_fields = ('get_user',)
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'
    #pass

class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'order',)
    search_fields = ('get_user',)   
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'


admin.site.register(User, CareUserAdmin)
admin.site.register(VerifiedInformation, VerifiedInformationAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)
