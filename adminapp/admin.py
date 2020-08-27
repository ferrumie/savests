# import
from django.contrib import admin
from django.contrib.auth.models import User
from .models import customUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
import datetime
from datetime import timezone


class testUserAdmin(admin.StackedInline):
    ''' custom Useradmin'''
    model = customUser


class MyAdminSite(AdminSite):
    ''' Admin site overide '''
    index_template = 'admin/adminapp/index.html'

    def index(self, request, extra_context=None):
        ''' metric view'''
        extra_context = extra_context or {}
        last_24_hours = {}
        last_month = {}
        last_year = {}
        days = []
        user_name = []
        for user in User.objects.all():
            user_name.append(user.username)
            # formating the date_joined time
            current = datetime.datetime.now(timezone.utc) - user.date_joined
            days.append(current.days)
            if user.date_joined:
                if current.days <= 1:
                    last_24_hours[user] = current.days
                if current.days <= 31:
                    last_month[user] = current.days
                if current.days <= 366:
                    last_year[user] = current.days
    # appending data to extra context   
        extra_context['last_24_hours'] = last_24_hours
        extra_context['last_month'] = last_month
        extra_context['last_year'] = last_year
        extra_context['days'] = days
        extra_context['users'] = user_name
        return super(MyAdminSite, self).index(request, extra_context=extra_context)


admin = MyAdminSite(name='myadmin')


class CustomAdmin(UserAdmin):
    '''inline set for user model '''
    inlines = (testUserAdmin, )
    list_display = (
        'username',
        'email',
        'is_active',
    )
    change_list_template = 'admin/adminapp/change_list.html'

    def toggle_true(self, request, queryset):
        '''function to toggle user_isactive from the django admin action dropdown'''
        for i in queryset:
            if i.is_active:
                queryset.update(is_active=False)
            else:
                queryset.update(is_active=True)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomAdmin, self).get_inline_instances(request)

    admin.add_action(toggle_true, "Toggle Active User") 


admin.site_header = "Savests Admin Dashboard"  # custom site header
admin.index_title = "Admin Metric "  # custom index_title
admin.site_title = "Savests"  # custom site title
admin.register(User, CustomAdmin)  # registering model
