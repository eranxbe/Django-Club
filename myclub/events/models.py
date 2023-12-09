from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField('Address', max_length=200)
    zip_code = models.CharField('Zip Code', max_length=10)
    phone = models.CharField('Phone', max_length=13, blank=True)
    website = models.URLField('Website', blank=True)
    email = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    image = models.ImageField('Image', null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name

class ClubUser(models.Model):
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=50)
    email = email = models.EmailField('Email Address')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(ClubUser, blank=True)
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name
    
    @property
    def days_until(self):
        today = date.today()
        days_till = self.event_date.date()
        return str(days_till - today).split(',', 1)[0]
