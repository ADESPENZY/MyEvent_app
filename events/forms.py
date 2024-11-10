from django import forms
from django.forms import ModelForm
from .models import Event, Venue, MyClubUser
from django.contrib.auth.models import User

# create a venue Form

class VenueForm(ModelForm):
    name = forms.CharField(label="Venue Name", widget=forms.TextInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    address = forms.CharField(label="Address", widget=forms.TextInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    zip_code = forms.CharField(label="Zip Code", widget=forms.TextInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    phone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    web = forms.URLField(label="Website", required=False, widget=forms.URLInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    email_address = forms.EmailField(label="Email Address", required=False, widget=forms.EmailInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    image = forms.ImageField(label="Image", required=False, widget=forms.FileInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))

    class Meta:
        model = Venue
        fields = ['name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'image']

        
#admin superuser event form
class EventFormAdmin(forms.ModelForm):
    name = forms.CharField(label="Event Name", widget=forms.TextInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    event_date = forms.DateTimeField(label="Event Date", widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    venue = forms.ModelChoiceField(queryset=Venue.objects.all(), label="Venue", required=False, widget=forms.Select(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    manager = forms.ModelChoiceField(queryset=User.objects.all(), label="Manager", required=False, widget=forms.Select(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green',
        'rows': 4
    }))
    attendees = forms.ModelMultipleChoiceField(
        queryset=MyClubUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Attendees",
        required=False
    )
    max_attendees = forms.IntegerField(
        label="Maximum Attendees",
        widget=forms.NumberInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
        }),
        required=False
    )

    class Meta:
        model = Event
        fields = ['name', 'event_date', 'venue', 'manager', 'description', 'attendees', 'max_attendees']

# user event form
class EventForm(forms.ModelForm):
    name = forms.CharField(label="Event Name", widget=forms.TextInput(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    event_date = forms.DateTimeField(label="Event Date", widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    venue = forms.ModelChoiceField(queryset=Venue.objects.all(), label="Venue", required=False, widget=forms.Select(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
    }))
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea(attrs={
        'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green',
        'rows': 4
    }))
    attendees = forms.ModelMultipleChoiceField(
        queryset=MyClubUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Attendees",
        required=False
    )
    max_attendees = forms.IntegerField(
        label="Maximum Attendees",
        widget=forms.NumberInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-forest-green'
        }),
        required=False
    )

    class Meta:
        model = Event
        fields = ['name', 'event_date', 'venue', 'description', 'attendees', 'max_attendees']

from django import forms
from .models import MyClubUser

class EventRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter your email'
        })
    )
    
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter your last name'
        })
    )

    class Meta:
        model = MyClubUser
        fields = ('first_name', 'last_name', 'email')
