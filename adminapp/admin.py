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
from django.contrib.admin import AdminSite
from django.conf.urls import url
from django.contrib.admin.apps import AdminConfig
from django.template.response import TemplateResponse
import datetime
from datetime import timezone
# Register your models here.

# admin.site.index_template = "admin/adminapp/admin_index.html"

class testUserAdmin(admin.StackedInline):
    model = customUser


# class MyAdminConfig(AdminConfig):
#     default_site = 'my_project.apps.MyAdminSite'
# class indexSite(AdminSite):
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('my_view/',  self.admin_site.admin_view(self.my_view)),
#         ]
#         return my_urls + urls

#     def my_view(self, request):
#         # ...
#         user = User.objects.all()
#         context = dict(
#            # Include common variables for rendering the admin template.
#            self.admin_site.each_context(request),
#            user
           
#         )
#         return TemplateResponse(request, "admin/adminapp/admin_index.html", context)



class MyAdminSite(AdminSite):
    index_template = 'admin/adminapp/index.html'
    def index(self, request, extra_context=None):
        # date_past_24_hours = datetime.datetime.now() - datetime.timedelta(days=1)
        # date_past_month = datetime.datetime.now() - datetime.timedelta(days=30)
        # date_past_year = datetime.datetime.now() - datetime.timedelta(days=365)
        # print(date_past_month)
        extra_context = extra_context or {}
        last_24_hours = {}
        last_month = {}
        last_year = {}
        days = []
        user_name = []
        for user in User.objects.all():
            user_name.append(user.username)
            current =datetime.datetime.now(timezone.utc) - user.date_joined
            days.append(current.days)
            if user.date_joined:
                if current.days <= 1:
                    last_24_hours[user] = current.days
                if current.days <= 31:
                    last_month[user] = current.days
                if current.days <= 366:
                    last_year[user] = current.days
                #  current.days <= 31:
                #     last_month.append(user)
            # if user.date_joined:
            #     if user.date_joined.replace(tzinfo=utc) >= date_past_24_hours.replace(tzinfo=utc):
            #         last_24_hours.append(user)
            #     elif user.date_joined>= date_past_month.replace(tzinfo=utc):
            #         last_month.append(user)
            #     elif user.date_joined >= date_past_year.replace(tzinfo=utc):
            #         last_year.append(user)
        
        extra_context['last_24_hours'] = last_24_hours
        extra_context['last_month'] = last_month
        extra_context['last_year'] = last_year
        extra_context['days'] = days
        extra_context['users'] = user_name
        print(extra_context)
        return super(MyAdminSite, self).index(request, extra_context=extra_context)


admin = MyAdminSite(name='myadmin')



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
            if i.is_active is True:
                queryset.update(is_active=False)
            elif i.is_active is False:
                queryset.update(is_active=True)
                

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomAdmin, self).get_inline_instances(request)

    # def send_email(self, request, queryset):
    #     form = SendEmailForm(initial={'users': queryset})
    #     return render(request, 'admin/adminapp/send_email.html', {'form': form})

    admin.add_action(toggle_true, "Toggle Active User") 
    # admin.site.add_action(toggle_false, "Make User Inactive") 
# admin.unregister(User)
admin.site_header = "Savests Admin Dashboard"
admin.index_title = "Admin Metric "
admin.register(User, CustomAdmin)
