from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Event  # Asegúrate de importar tu modelo de evento
import json
from .forms import EventForm
from django.views.decorators.csrf import csrf_exempt

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            # Aquí podrías manejar la configuración de las sillas si es necesario
            return redirect('event_detail', event_id=event.id)  # Redirigir a la vista de detalles del evento
    else:
        form = EventForm()
    
    return render(request, 'pages/configure_event.html', {'form': form})

@csrf_exempt
def save_configuration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        configuracion = data.get('configuracion', {})

        # Aquí deberías guardar la configuración en tu modelo
        event = Event.objects.create(
            nombre='Nombre del evento',  # Cambia esto según sea necesario
            fecha='2024-10-11',          # Cambia esto según sea necesario
            configuracion=configuracion
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
