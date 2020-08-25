from django.contrib import admin
from django.contrib.auth.models import User
from .models import customUser
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path
from . import views
from django.shortcuts import render
from .forms import SendEmailForm
from django.core.mail import send_mail
# Register your models here.

class testUserAdmin(admin.StackedInline):
    model = customUser
    

class CustomAdmin(UserAdmin):
    inlines = (testUserAdmin, )
    list_display = (
        'username',
        'email',
        'is_active',
    )
    change_list_template = 'admin/adminapp/change_list.html'
 
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

    # def send_email(self, request, queryset):
    #     form = SendEmailForm(initial={'users': queryset})
    #     return render(request, 'admin/adminapp/send_email.html', {'form': form})

    admin.site.add_action(toggle_true, "Toggle Active User") 
    # admin.site.add_action(toggle_false, "Make User Inactive") 
admin.site.unregister(User)
admin.site.register(User, CustomAdmin)