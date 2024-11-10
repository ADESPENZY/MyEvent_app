from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from datetime import date, datetime

# Validator function to check file extension
def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # Extract the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Define allowed extensions
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: .jpg, .png, .jpeg, .webp')

# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=20, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', max_length=200, blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    image = models.ImageField(
        'Image Field',
        null=True,
        blank=True,
        upload_to="images/",
        validators=[validate_image_extension],  # Add the validator here
    )

    def __str__(self):
        return self.name
    
class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    approved = models.BooleanField('Approved', default=False)
    max_attendees = models.PositiveIntegerField(default=0)  # New field

    def __str__(self):
        return self.name
    
    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_stripped = str(days_till).split(",",1)[0]
        return days_till_stripped
    
    @property
    def attendees_count(self):
        return self.attendees.count()
    
    @property
    def spots_left(self):
        return self.max_attendees - self.attendees_count

    # @property
    # def is_past(self):
    #     today = datetime.now()  # Changes 'today' to a datetime object
    #     if self.event_date < today:
    #         return "past"
    #     else:
    #         return "upcoming"