from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from event.models import Chair, Event
from .models import Reservation
from .forms import ReservationForm
from django.urls import reverse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class EventDetailView(DetailView):
    model = Event
    template_name = 'reservation_index.html'
    queryset = Event.objects.all()
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'].configuracion = json.loads(context['event'].configuracion)
        context['chairs'] = len(context['event'].configuracion['sillas'])
        return context

    
    
class ReservationCreateView(CreateView):
    model = Reservation
    template_name = 'reservation_create.html'
    form_class = ReservationForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse ('home:index')
    
@csrf_exempt  # Necesario si usas fetch POST con JSON
def reservar_asientos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_seats = data.get('seats', [])
            print(f"Recibidos: {selected_seats}")

            # Lógica para guardar la reservación de asientos
            for seat in selected_seats:
                # Aquí puedes guardar la reservación de cada asiento en la base de datos
                # Por ejemplo, crear una instancia de tu modelo de Reservación
                # Reservation.objects.create(seat_number=seat, user=request.user)

                print(f"Asiento {seat} reservado")  # Imprime para verificar que se reciben los asientos

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def test(request):
    return render(request, 'test.html')