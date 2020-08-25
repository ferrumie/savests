from django.contrib import admin
from django.contrib.auth.models import User
from .models import customUser
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path
from . import views

# Register your models here.

class testUserAdmin(admin.StackedInline):
    model = customUser
    

class CustomAdmin(UserAdmin):
    inlines = (testUserAdmin, )
    list_display = (
        'id',
        'username',
        'is_active',
    )
 
    def toggle_true(self, request, queryset):
        for i in queryset:
            if i.is_active == True:
                queryset.update(is_active=False)
            elif i.is_active == False:
                queryset.update(is_active=True)
                

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomAdmin, self).get_inline_instances(request)

    admin.site.add_action(toggle_true, "Toggle Active User") 
    # admin.site.add_action(toggle_false, "Make User Inactive") 
admin.site.unregister(User)
admin.site.register(User, CustomAdmin)