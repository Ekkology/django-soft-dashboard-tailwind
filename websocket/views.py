from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from event.models import chair, Event
from .models import Reservation
from .forms import ReservationForm
from django.urls import reverse

# Create your views here.
class EventDetailView(DetailView):
    model = Event
    template_name = 'reservation_index.html'
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chairs'] = chair.objects.filter(evento=self.object)
        return context
    
    def get_object(self):
        return Event.objects.get(pk=self.kwargs['pk'])
    
class ReservationCreateView(CreateView):
    model = Reservation
    template_name = 'reservation_create.html'
    form_class = ReservationForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse ('home:index')