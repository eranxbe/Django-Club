from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.

admin.site.unregister(Group)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')

@admin.register(ClubUser)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    ordering = ('last_name',)
    search_fields = ('first_name', 'last_name', 'email')    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'venue', 'event_date', 'description', 'manager', 'approved')
    list_display = ('name', 'venue', 'event_date')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)

    


