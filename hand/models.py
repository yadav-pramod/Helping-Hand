from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages 

# Create your models here.
class hospital(models.Model):

    class area(models.TextChoices):
            Kathmandu='Kathmandu'
            Janakpur = 'Janakpur'
            Pokhara = 'Pokhara' 
            Dhulikhel='Dhulikhel'


    class is_a(models.TextChoices):
            Hospital='Hospital'
            Hotel = 'Hotel'
            School = 'School'  
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    currently_a =models.CharField(choices=is_a.choices,default=is_a.Hospital,max_length=20)
    no_of_rooms=models.IntegerField()
    name=models.CharField( max_length=100)
    region =models.CharField(choices=area.choices,max_length=100)
    adress=models.CharField( max_length=500)
    location=models.URLField( max_length=5000)
    image=models.ImageField( upload_to='hospital')
    contact_info=models.CharField( max_length=50)
    website=models.CharField( max_length=1000)
    no_of_doctor=models.IntegerField()
    no_of_beds_available=models.IntegerField()
    class corona(models.TextChoices):
        Yes = 'Yes'
        No = 'No'
    corona_test_availability=models.CharField( choices=corona.choices,max_length=20)
    class show(models.IntegerChoices):
        yes = 1
        no = 0
        
    allowed=models.IntegerField(choices=show.choices,default=show.no)
    
             
    

    
    
    
    
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        
        return reverse('user-hospital', kwargs={'username': self.author})




class delete_request(models.Model):

    hospital_info = models.ForeignKey(hospital, on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    email=models.EmailField()
    hospital_id=models.IntegerField()
    hospital_name=models.CharField(max_length=100)
    why=models.CharField( max_length=5000)
    
   
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField( max_length=50)
    citizenship_no=models.CharField( max_length=50)
    

    

    def __str__(self):
        return self.name

class feedback (models.Model):

    name=models.CharField(max_length=100)
    email=models.EmailField(null=True)
    message=models.CharField( max_length=5000)


    
    

    class Meta:
        verbose_name = "feedback"
        verbose_name_plural = "feedback"

    def __str__(self):
        return self.name

    
