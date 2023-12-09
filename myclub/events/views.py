from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import *
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import csv
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def calendar_event(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = request.user.username if request.user.is_anonymous else ""
    print(name)
    month_num = list(calendar.month_name).index(month.title())

    cal = HTMLCalendar().formatmonth(int(year), int(month_num))

    now = datetime.now()
    current_year = now.year

    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_num
        )

    time = now.strftime('%H:%M')
    return render(request, 'calendar.html', {
        "name": name,
        "year": current_year,
        "month": month,
        "month_num": month_num,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        "events": event_list
    })

def my_events(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(attendees=request.user.id)
        return render(request, 'my_events.html', {"me": request.user.id, "events": events})
    else:
        messages.success(request, 'You are not authorized to view this page')
        return redirect('index')
    # return render(request, 'my_events.html', {'events': events})

def events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events.html', {
        "events": event_list
    })

def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            event = form.save(commit=False)
            event.manager = request.user
            event.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
        else:
            form = EventForm(request.POST)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_event.html', {
        "form": form,
        "submitted": submitted,
    })


def venues(request):
    # venue_list = Venue.objects.all().order_by('?') - random order
    venue_list = Venue.objects.all().order_by('-name')

    # set up pagination
    p = Paginator(venue_list, per_page=2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    return render(request, 'venues.html', {
        "venues_list": venue_list,
        "venues": venues
    })

def venue_details(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    owner = User.objects.get(pk=venue.owner)
    events = venue.event_set.all()
    return render(request, 'venue_details.html', {"venue": venue, "owner": owner, "events": events})

def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'search_venues.html', {
            "searched": searched,
            "venues": venues,
        })
    else:
        return render(request, 'search_venues.html', {})
    
def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'search_events.html', {
            "searched": searched,
            "events": events,
        })
    else:
        return render(request, 'search_events.html', {})

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id # logged in user
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_venue.html', {
        "form": form,
        "submitted": submitted,
    })

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venues')
    return render(request, 'update_venue.html', {
        "venue": venue,
        "form": form,
    })

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:    
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events')
    return render(request, 'update_event.html', {
        "event": event,
        "form": form,
    })  

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event deleted successfully")
    else:
        messages.success(request, "You are not allowed to delete this event")
    return redirect('events')

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if request.user == venue.owner:
        venue.delete()
        messages.success(request, "Venue deleted successfully")
    else:
        messages.success(request, "You are not allowed to delete this venue")
    return redirect('venues')

def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()
    response.writelines([f'{venue}\n' for venue in venues])
    return response

def users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=users.csv'
    writer = csv.writer(response)
    users = ClubUser.objects.all()

    writer.writerow(['First Name', 'Last Name', 'Email'])
    for user in users:
        writer.writerow([user.first_name, user.last_name, user.email])
    return response

def events_pdf(request):
    # create bytestream buffer
    buf = io.BytesIO()
    # create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create text obect
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    events = Event.objects.all()
    lines = []
    for event in events:
        line = [f'{event.name}', f'{event.event_date}', f'{event.venue}', f'{event.manager}', f'{event.description}', "==============="]
        lines.append(line)

    for line in lines:
        for prop in line:
            textob.textLine(prop)

    # lines = [f'{i} fucks I give' for i in range(1, 6)]
    # for line in lines:
    #     textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='events.pdf')

def admin_approval(request):
    event_count = Event.objects.count()
    venue_count = Venue.objects.count()
    user_count = User.objects.count()
    venue_list = Venue.objects.all()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            event_list.update(approved=False)
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, 'Event List Approval Updated')
            return redirect('events')
        else:
            return render(request, 'admin_approval.html', {
                'event_list': event_list,
                'event_count': event_count,
                'venue_count': venue_count,
                'user_count': user_count,
                'venue_list': venue_list})
    else:
        messages.success(request, 'You are not authorized to view this page')
        return redirect('home')

def venue_event(request, venue_id):
    venue = Venue.objects.get(id=int(venue_id))
    events = venue.event_set.all()
    if events:
        return render(request, 'venue_event.html', {
            "events": events,
        })
    else:
        messages.success(request, "This venue has no events")
        return redirect('admin_approval')       
    