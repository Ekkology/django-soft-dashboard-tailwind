from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Event, chair  # Importa tu modelo de silla (Chair)
from .forms import EventForm
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
import json

@csrf_exempt
def create_event_and_save_configuration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_data = data.get('event')
            configuracion = data.get('configuracion')

            form = EventForm(event_data)
            if form.is_valid():
                with transaction.atomic():
                    evento = form.save()

                    for silla_data in configuracion.get('sillas', []):
                        numero = silla_data.get('numero')
                        posicion = silla_data.get('posicion')

                        if not numero or not isinstance(numero, int) or numero <= 0:
                            return JsonResponse({'error': 'Número de silla inválido.'}, status=400)

                        try:
                            chair.objects.create(
                                numero=numero,
                                posicion_x=posicion['x'],
                                posicion_y=posicion['y'],
                                evento=evento
                            )
                        except IntegrityError:
                            return JsonResponse({'error': f'Número de silla {numero} ya existe.'}, status=400)

                return JsonResponse({'success': True})

            return JsonResponse({'error': 'Datos del evento inválidos.', 'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
from django.shortcuts import render

def show_event_form(request):
    form = EventForm()  # Suponiendo que tienes un formulario de eventos llamado EventForm
    return render(request, 'pages/event_form.html', {'form': form})