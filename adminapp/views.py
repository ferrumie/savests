from django.shortcuts import render
from .forms import SendEmailForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail


class SendUserEmails(FormView):
    ''' view for sending email'''
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