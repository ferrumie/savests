from django.shortcuts import render
from .forms import SendEmailForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.
'''


Ose Iyoke (SaVests) <ose@savests.com>
3:00 PM (3 hours ago)
to ose, bcc: me

Hello,

Congratulations! Your Django backend application was received and you've been selected for the next round of interview. Below is a mini task to help us understand your skillset better.
If you have any questions or clarifications to make don't hesitate to contact me here.

Your task is to extend the Django-admin user interface doing the following:
Create a superuser with credentials username: root password: password done
Extend the Django admin dashboard page to show user metrics, example is the number of users created over the past 24hours, past week and past month. (You can add additional metrics to the admin dashboard at your discretion). 
Add a custom action button to the users list page that enables staff to set a user to active or inactive with the click of a button. (You can add additional useful functionalities to the admin users list page at your discretion).
Add a functionality page that allows staff to send an email to all existing users. You can/should use Django's console.EmailBackend to send the emails.
Please don't forget to add your db.sqlite3 file to your repo.
Host your code on Heroku or any PAAS of your choice
Reply this email with a URL link to your app and repo on or before Thursday 27th August 2020.
What we will evaluate:
Functional completeness.
Code quality and modularity
Application organization across files and within each file - please ensure you follow the framework standards et cetera.
Thank you and best of luck!
SaVests Eng. Team.
'''

class SendUserEmails(FormView):
    template_name = 'admin/adminapp/send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('admin:auth_user_changelist')
    
    def form_valid(self, form):
    #    users = form.cleaned_data['users']
        users = User.objects.all()
        email = []
        for user in users:
            email.append(user.email)
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
   #    email_users.delay(users, subject, message)
        send_mail(subject, message, 'no-reply@djangointern.com', email, fail_silently=False)
        user_message = 'users emailed successfully!'
        messages.success(self.request, user_message)
        return super(SendUserEmails, self).form_valid(form)

def admin_view(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, '/admin/dminapp/admin_index.html', context)