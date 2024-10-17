from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Event, Chair  # Asegúrate de que la ruta de importación sea correcta
from .forms import EventForm
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
import json

@csrf_exempt
def create_event_and_save_configuration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)

            event_data = data.get('event')
            configuracion = data.get('configuracion')

            # Convertir 'num_sillas' a entero y generar la lista de sillas
            num_sillas = int(event_data.get('num_sillas', 0))
            print("Número de sillas:", num_sillas)

            configuracion['sillas'] = [i for i in range(1, num_sillas + 1)]
            print("Sillas generadas:", configuracion['sillas'])

            # Inicializar el formulario con los datos del evento
            form = EventForm(event_data)
            if form.is_valid():
                
                with transaction.atomic():
                    print("llego")
                    form.instance.configuracion=json.dumps(configuracion)
                    evento = form.save()
                return JsonResponse({'success': True})

            print("Errores del formulario:", form.errors)
            return JsonResponse({'error': 'Datos del evento inválidos.', 'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            print(f"Error inesperado: {e}")
            return JsonResponse({'error': 'Error interno del servidor.'}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def show_event_form(request):
    form = EventForm()  # Suponiendo que tienes un formulario de eventos llamado EventForm
    return render(request, 'pages/event_form.html', {'form': form})
