from django.urls import path
from .views import create_event, save_configuration

urlpatterns = [
    path('event/create/', create_event, name='crear_evento'),
    path('save_configuration/', save_configuration, name='save_configuration'),
]