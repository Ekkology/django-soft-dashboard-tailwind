from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from event.models import Chair, Event
from .models import Reservation,Chair, Event
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
        context['ya_ocupe_silla'] = Chair.objects.filter(evento=context['event'])
        context['ya_ocupe_silla_numeros'] = [silla.numero for silla in context['ya_ocupe_silla']]
        #print(context['ya_ocupe_silla'])
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
            event_id = data.get('event_id')

            if not selected_seats:
                return JsonResponse({'error': 'No has seleccionado ningún asiento.'}, status=400)

            # Obtener el evento correspondiente
            event = Event.objects.get(id=event_id)
            
            for seat_id in selected_seats:
                user_id = request.user.id

                existing_chair = Chair.objects.filter(numero=seat_id, evento=event).first()

                if existing_chair:
                    return JsonResponse({'error': 'Silla registrada'}, status=404)

                # Crear o buscar la silla
                chair = Chair()
                chair.posicion_y=1
                chair.posicion_x=1
                chair.numero = seat_id  # Asigna el ID del asiento
                chair.evento = event  # Asegúrate de que el campo es una relación con Event
                chair.estado = 'ocupado'  # Establece el estado como 'ocupado'
                chair.save()

                # Crear la reservación
                reservation = Reservation()
                reservation.chair = chair  # Aquí asignamos el objeto chair
                reservation.id_event = event  # Asigna el ID del evento
                reservation.id_user = request.user  # Asigna el ID del usuario
                reservation.save()

            return JsonResponse({'success': True, 'message': '¡Asientos reservados con éxito!'})
        
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado.'}, status=404)
        except Chair.DoesNotExist:
            return JsonResponse({'error': 'Asiento no encontrado.'}, status=404)
        except Exception as e:





            print(f"Error: {e}")  # Para depuración
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
def test(request):
    return render(request, 'test.html')

