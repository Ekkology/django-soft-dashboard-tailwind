from django.urls import path, include
from . import views

urlpatterns = [
    path('detail/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
]