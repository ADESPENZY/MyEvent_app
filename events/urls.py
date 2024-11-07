from django.urls import path
from . import views

urlpatterns = [
    # int: numbers
    # str: strimgs
    # path: whole urls /
    # slug: hyphen-and _underscores_stuff
    # UUID: universal unique identifier

    path('', views.home, name='event-home-page'),
    path('<int:year>/<str:month>/', views.home, name='event-home-page'),
    path('all_events/', views.all_events, name='events-list'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('list_venue/', views.list_venue, name='list-venue'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('search/', views.search, name='search'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('add_event/', views.add_event, name='add-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),
    path('my_events', views.my_events, name='my-events'),
    path('event_registration/<int:event_id>/', views.event_registration, name='event-registration'),
    path('admin_approval', views.admin_approval, name='admin-approval'),
    path('events-by-venue/<int:venue_id>/', views.events_by_venue, name='events-by-venue'),
]