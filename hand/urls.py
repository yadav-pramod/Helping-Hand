from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as mail_urls
from . import views
from .views import (
    HospitalCreateView,
    HospitalUpdateView,
    UserHospitalListView,

)   

urlpatterns = [
   
    path('corona/',views.corona,name='corona'),
    path('login/',views.login1,name='login1'),
    path('register/',views.register,name='register'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('logout/',views.logoutuser,name='logout'),
    path('foruser/',views.foruser,name='foruser'),
    path('guidlines/',views.guide,name='guide'),   
    path('delete_requests/',views.delete_requests,name='delete_requests'),
    path('allow/',views.allow,name='allow'),
    path('about/',views.about,name='about'),
    path('feedback/',views.user_feedback,name='feedback'),
    path('hospital/<int:pk>/del/', views.delete_info, name='hospital-del'),
    path('', views.home, name='home_1'),
    path('user/<str:username>', UserHospitalListView.as_view(), name='user-hospital'),
    path('hospital/<int:pk>/update/', HospitalUpdateView.as_view(), name='hospital-update'),
    path('hospital/new/', HospitalCreateView.as_view(), name='hospital-create'),
    path('email/', include(mail_urls)),
    
]