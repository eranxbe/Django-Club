from django.urls import path
from . import views


"""
    Path Converters:
        int: numbers
        str: string
        path: /
        slug: - _
        UUID: univeral unique identifier
"""

urlpatterns = [
    path('', views.index, name='home'),
    path('calendar_event', views.calendar_event, name='calendar_event'),
    path('events', views.events, name='events'),
    path('add_venue', views.add_venue, name='add_venue'),
    path('venues', views.venues, name='venues'),
    path('venues/<str:venue_id>', views.venue_details, name='venue_details'),
    path('search_venues', views.search_venues, name='search_venues'),
    path('venue/<str:venue_id>/update', views.update_venue, name='update_venue'),
    path('add_event', views.add_event, name='add_event'),
    path('events/<str:event_id>/update', views.update_event, name='update_event'),
    path('delete_event/<str:event_id>', views.delete_event, name='delete_event'),
    path('delete_venue/<str:venue_id>', views.delete_venue, name='delete_venue'),
    path('venue_text', views.venue_text, name='venue_text'),
    path('users_csv', views.users_csv, name='users_csv'),
    path('events_pdf', views.events_pdf, name='events_pdf'),
    path('my_events', views.my_events, name='my_events'),
    path('search_events', views.search_events, name='search_events'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('venue_event/<venue_id>', views.venue_event, name='venue_event'),

]
