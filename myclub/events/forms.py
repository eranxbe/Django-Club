from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# Admin/superuser event form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description')
        labels = {
            "name": "Event Name",
            "event_date": "Event Date YYYY-MM-DD HH:mm",
            "venue": "Venue",
            "manager": "Manager",
            "attendees": "Attendees",
            "description": "Description",
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "event_date": forms.TextInput(attrs={'class': 'form-control'}),
            "venue": forms.Select(attrs={'class': 'form-select'}),
            "manager": forms.Select(attrs={'class': 'form-select'}),
            "attendees": forms.SelectMultiple(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
        }

# normal user event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'attendees', 'description')
        labels = {
            "event_date": "Event Date YYYY-MM-DD HH:mm",
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "event_date": forms.TextInput(attrs={'class': 'form-control'}),
            "venue": forms.Select(attrs={'class': 'form-select'}),
            "attendees": forms.SelectMultiple(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
        }        

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'website', 'email', 'image')
        # labels = {
        #     "name": "Venue Name",
        #     "address": "Address",
        #     "zip_code": "Zip Code",
        #     "phone": "Phone Number",
        #     "website": "Website",
        #     "email": "Email Address",
        # }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            "zip_code": forms.TextInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "website": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.TextInput(attrs={'class': 'form-control'}),
        }


