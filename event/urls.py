from django.urls import path
from .views import create_event_and_save_configuration, show_event_form

urlpatterns = [
   path('create_event_and_save_configuration/', create_event_and_save_configuration, name='create_event_and_save_configuration'),
   path('create_event_form/', show_event_form, name='show_event_form'),
]