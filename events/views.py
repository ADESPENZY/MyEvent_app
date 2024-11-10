from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import calendar
from django.contrib import messages
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin, EventRegistrationForm
from django.http import HttpResponse, HttpResponseForbidden
import csv
# paginator installment
from django.core.paginator import Paginator

# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Adespenzy"
    month = month.title()
    # convert month from name to number 
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    
    # get current year
    now = datetime.now()
    current_year = now.year

    # query event model for dates
    event_list = Event.objects.filter(event_date__year = year, event_date__month = 11)

    # get current time 
    time = now.strftime('%I:%M %p')

    context = {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time, 
        "event_list": event_list,
    }
    return render(request, 'events/home.html', context)

def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html', {'event_list': event_list})

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid:
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted=True
    return render(request, 'events/add_venue.html', {'form': form, 'submitted':submitted})

def list_venue(request):
    # venue_list = Venue.objects.all().order_by('name')

    # set up pagnation
    p = Paginator(Venue.objects.all(), 3)
    page = request.GET.get('page')
    venues = p.get_page(page)
    return render(request, 'events/venue_list.html', {'venues':venues})

def show_venue(request, venue_id):
    show_venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=show_venue.owner)
    events = Event.objects.filter(venue=show_venue)
    return render(request, 'events/show_venue.html', {'show_venue': show_venue, 'venue_owner':venue_owner, 'events':events})

def update_venue(request, venue_id):
    update_venue = Venue.objects.get(pk=venue_id)
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=update_venue)
        if form.is_valid():
            form.save()
            return redirect('list-venue')  # Adjust the redirect as needed
    else:
        form = VenueForm(instance=update_venue)  # Prepopulate the form with existing data if GET request
    
    return render(request, 'events/update_venue.html', {"update_venue": update_venue, 'form': form})


def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.manager and not request.user.is_superuser:
        # If the user is not authorized, return a 403 Forbidden response
        return HttpResponseForbidden("You are not allowed to edit this event.")
    if request.method == 'POST':
        if request.user.is_superuser:
           form = EventFormAdmin(request.POST, instance=event)
        else:
            form = EventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect('events-list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form, 'event':event})

def my_events(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(manager=request.user)
        return render(request, 'events/my_events.html', {'events': events})
    else:
        messages.error(request, 'You aren’t authorized to view this page')
        return render(request, 'events/my_events.html', {})

def event_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    submitted = False

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            my_club_user = form.save()
            
            # Add the user to the event's attendees
            event.attendees.add(my_club_user)

            # Use `reverse` here to generate the URL dynamically
            return HttpResponseRedirect(reverse('event-registration', args=[event.id]) + '?submitted=True')
    else:
        form = EventRegistrationForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/event_registration.html', {
        'form': form,
        'event': event,
        'submitted': submitted,
    })

def admin_approval(request):
    # get counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    event_list = Event.objects.all().order_by('event_date')
    venue_list = Venue.objects.all().order_by('name')
    
    if request.user.is_superuser:
        if request.method == 'POST':
            # Get the list of approved event IDs from the form
            approved_ids = request.POST.getlist('approve[]')
            
            # Debugging: Print the approved_ids list to confirm if data is received
            print("Approved IDs:", approved_ids)
            
            # Update events: set approved for selected IDs, unapproved for others
            Event.objects.update(approved=False)  # Unapprove all events initially
            Event.objects.filter(id__in=approved_ids).update(approved=True)  # Approve selected events
            
            messages.success(request, 'Your event approval list has been updated!')
            return redirect('events-list')
        else:
            context= {
                'event_list': event_list,
                'venue_list': venue_list,
                'event_count':event_count,
                'venue_count':venue_count,
                'user_count':user_count,
                }
            return render(request, 'events/admin_approval.html', context)
    
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('event-home-page')
    
def events_by_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    events = Event.objects.filter(venue=venue).order_by('event_date')
    context = {
        'venue': venue,
        'events': events,
    }
    return render(request, 'events/events_by_venue.html', context)


def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        # Use icontains for case-insensitive search
        venues = Venue.objects.filter(name__icontains=query)
        events = Event.objects.filter(name__icontains=query)
        return render(request, 'events/search.html', {'query': query, 'venues': venues, 'events': events})
    else:
        return render(request, 'events/search.html')

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
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True') 
    else:
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()
        if 'submitted' in request.GET:
            submitted=True
    return render(request, 'events/add_event.html', {'form': form, 'submitted':submitted})

def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        if request.user == event.manager or request.user.is_superuser:
            event.delete()
            messages.success(request, 'Event deleted successfully.')
        else:
            messages.error(request, 'You are not authorized to delete this event.')
        return redirect('events-list')

def delete_venue(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    if request.method == 'POST':
        venue.delete()
        return redirect('list-venue')
    
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    
    # Fetch all venues
    venues = Venue.objects.all()

    # Create a list to store each venue's details as formatted strings
    lines = []

    # Loop through each venue and format its details
    for venue in venues:
        lines.append(
            f"Name: {venue.name}\n"
            f"Address: {venue.address}\n"
            f"Zip Code: {venue.zip_code}\n"
            f"Phone: {venue.phone}\n"
            f"Website: {venue.web}\n"
            f"Email: {venue.email_address}\n"
            "\n"  # Adds a blank line after each venue for readability
        )

    # Write lines to response
    response.writelines(lines)
    return response

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # create a csv writer
    writer = csv.writer(response)
    
    # Fetch all venues
    venues = Venue.objects.all()

    # add column headings to the csv files
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])

    # Loop through each venue and format its details
    for venue in venues:
        writer.writerow([
            venue.name,           # Venue name
            venue.address,        # Venue address
            venue.zip_code,       # Venue zip code
            venue.phone,          # Venue phone number
            venue.web,            # Venue website
            venue.email_address   # Venue email
        ])
    return response

from django.http import FileResponse
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def venue_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y_position = height - inch  # Starting position

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, y_position, "Venue List")
    y_position -= 0.5 * inch

    # Column headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(inch, y_position, "Name")
    p.drawString(3 * inch, y_position, "Address")
    p.drawString(5.5 * inch, y_position, "Zip Code")
    p.drawString(7 * inch, y_position, "Phone")
    y_position -= 0.3 * inch

    # Set spacing parameters
    line_spacing = 12  # Space between each line in address
    entry_spacing = 0.6 * inch  # Space between entries

    venues = Venue.objects.all()
    p.setFont("Helvetica", 10)

    for venue in venues:
        if y_position < inch:  # New page if space runs out
            p.showPage()
            y_position = height - inch
            p.setFont("Helvetica", 10)

        # Draw name
        p.drawString(inch, y_position, venue.name)

        # Wrap and draw address
        text_obj = p.beginText(3 * inch, y_position)
        text_obj.setFont("Helvetica", 10)
        text_obj.setLeading(line_spacing)
        address_lines = venue.address.split(', ')
        for line in address_lines:
            text_obj.textLine(line)
        p.drawText(text_obj)

        # Draw zip code and phone
        p.drawString(5.5 * inch, y_position, venue.zip_code)
        p.drawString(7 * inch, y_position, venue.phone)

        # Adjust y_position based on address height
        y_position -= (len(address_lines) * line_spacing) + entry_spacing

    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='venues.pdf')

from django.core.exceptions import ValidationError
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # Extract the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Add any other extensions you want to allow
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: .jpg, .jpeg, .png, .gif')

