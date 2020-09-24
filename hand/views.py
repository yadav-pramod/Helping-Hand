from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required 
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import hospital,delete_request,profile,feedback
from .forms import myform
from django.db.models import Q
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
from django_email_verification import *
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
# Create your views here.
def home(request):

    data={
            'hospitals':hospital.objects.all().order_by('-no_of_beds_available')
           }
    if request.method=='POST':
        if 'search_btn' in request.POST:
            search=request.POST.get('search')
            data={
                     'hospitals':hospital.objects.filter(name__contains=search).order_by('-no_of_beds_available')
                     }
        else:
               
            region=request.POST.get('region')
            if region=='All':
                
                data={
                       'hospitals':hospital.objects.all().order_by('-no_of_beds_available')
                     }
            else:

                data={
                       'hospitals':hospital.objects.filter(region=region).order_by('-no_of_beds_available')
                     }
    
    return render (request, 'hand/home.html',data)

def corona(request):
    
    return render  (request, 'hand/corona.html')

def about(request):
    
    return render  (request, 'hand/about.html')


def login1(request):


    taken=()
    for user in User.objects.values_list('username') :
        taken=taken+user
    data={
             'usernames':list(taken)
            } 

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        loginUser=authenticate(request,username=username,password=password)

        if loginUser is not None:
     
            login(request,loginUser)
            return redirect('user-hospital', username)
            
        else:
            messages.info(request,'Username or Password Is INCORRECT ')    
        
    return render (request,'hand/front.html',data)

def register(request):
       
    taken=()
    for user in User.objects.values_list('username') :
        taken=taken+user
    data={
            'usernames':list(taken)
                 }    

    if request.method=='POST':
        
        username=request.POST['username']
        email=request.POST['email']
        citizenship_no=request.POST['cno']
        password1=request.POST['password1']
        password2=request.POST['password1']
        name=request.POST['name']
        if password1==password2:

            user = get_user_model().objects.create(username=username, email=email)
            user.set_password(password1)
            user.is_active=False
            user.save()
            user_info= profile( user=user, name=name,citizenship_no=citizenship_no)
            user_info.save()
            current_site=get_current_site(request)
            mail_subject='Activate your  account.'
            message = render_to_string('hand/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            })
            
            email_activate = EmailMessage(

                mail_subject, 
                message, 
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_activate.fail_silently=False
            email_activate.send()
            return HttpResponse('Please confirm your email address to complete the registration.A mail has been sent to your email address with the conformation link')
    
    return render (request,'hand/front.html',data)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def logoutuser(request):
    logout(request)
    return redirect('home_1')    

@login_required
def delete_info(request,pk):
    h = hospital.objects.get(  id = pk)
    if request.method=='POST':
               
            author=h.author
            name=h.name                    
            username=request.user.username
            email=request.user.email            
            why=request.POST['why']
            if request.user == author:
                hospital_id=pk
                hospital_name=name
                s=delete_request(hospital_info=h,username=username,email=email,hospital_id=hospital_id,hospital_name=hospital_name,why=why)
                s.save()
                messages.success(request,f'Delete request for {hospital_name}! has been submitted ')
                return redirect ('user-hospital',username)
            return False   
    return render (request,'hand/del.html')

# hospitals
    
class UserHospitalListView(ListView):
    model = hospital
    template_name = 'hand/foruser.html'
    context_object_name = 'hospitals'
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return hospital.objects.filter(author=user)


class HospitalCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = hospital
    fields = ['currently_a','no_of_rooms','name','region', 'adress','location','image','contact_info','website','no_of_doctor','no_of_beds_available','corona_test_availability']
    success_message = "Request to add %(name)s was submitted successfully"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        

class HospitalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = hospital
    fields = ['name', 'adress','location','image','contact_info','website','no_of_doctor','no_of_beds_available','corona_test_availability']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        hospital = self.get_object()
        if self.request.user == hospital.author:
            return True
        return False        


@login_required
def foruser(request):
    
    return render  (request, 'hand/foruser.html')
  
def guide(request):
    return render (request,'hand/guide.html')


@staff_member_required
def delete_requests(request):

    data={
        'reqs':delete_request.objects.all().order_by('-id')
    }

    if request.method=='POST':
        
        username=request.POST['username']
        email=request.POST['email']
        hospital_id=request.POST['hospital_id']
        hospital_name=request.POST['hospital_name']
        delete_request_id=request.POST['delete_request_id']
        hospital_delete=hospital.objects.get(id=hospital_id)
        hospital_delete.delete()
        instance = delete_request.objects.get(id=delete_request_id)
        instance.delete()
        mail_subject='Requested Hospital Successfully Deleted.'
        current_site=get_current_site(request)
        message = render_to_string('hand/superuser/delete_email.html', {
            'website':current_site,
            'user': username,
            'hospital':hospital_name
            
            })
            
        email_activate = EmailMessage(

            mail_subject, 
            message, 
            settings.EMAIL_HOST_USER,
            [email]
            )
        email_activate.fail_silently=False
        email_activate.send()
        return render  (request, 'hand/superuser/delete_requests.html',data)

    return render  (request, 'hand/superuser/delete_requests.html',data)        

@staff_member_required
def allow (request):

    data={
        'allows':hospital.objects.all().filter(allowed=0).order_by('-id')
    }

    if request.method=='POST':
        
        username=request.POST['username']
        email=request.POST['email']
        hospital_id=request.POST['hospital_id']
        hospital_name=request.POST['hospital_name']
        hospital_update=hospital.objects.filter(id=hospital_id)
        hospital_update.update(allowed=1)
        mail_subject='Requested Hospital Allowed.'
        current_site=get_current_site(request)
        message = render_to_string('hand/superuser/allow_email.html', {
            'website':current_site,
            'user': username,
            'hospital':hospital_name
            
            })
            
        email_activate = EmailMessage(

            mail_subject, 
            message, 
            settings.EMAIL_HOST_USER,
            [email]
            )
        email_activate.fail_silently=False
        email_activate.send()
        return render  (request, 'hand/superuser/allow.html',data)

    return render(request,'hand/superuser/allow.html',data) 
     
def user_feedback(request):
    if request.method=='POST':

        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        s=feedback(name=name,email=email,message=message)
        s.save()
        messages.success(request,f'Thank You for your feedback!')
        return redirect('about')





