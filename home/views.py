from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.forms import LoginForm, RegistrationForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import logout
from event.models import Event
from datetime import datetime
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/accounts/login/")
def index(request):
    # Filtrar eventos futuros (eventos cuya fecha es mayor o igual a la fecha actual)
    upcoming_events = Event.objects.filter(fecha__gte=datetime.now()).order_by('fecha')
    
    # Paginación: Mostrar 6 eventos por página
    paginator = Paginator(upcoming_events, 6)  # Cambiar '6' si quieres más o menos eventos por página
    page_number = request.GET.get('page')  # Obtener el número de la página actual desde la URL (si existe)
    page_obj = paginator.get_page(page_number)  # Obtener la página actual de eventos
    
    # Contexto a pasar a la plantilla
    context = {
        'parent': 'pages',
        'segment': 'index',
        'upcoming_events': upcoming_events,
        'page_obj': page_obj,  # Pasar el objeto de la página al contexto
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'pages/dashboard.html', context)



def event_view(request, event_id):
    return render(request, 'layouts/event.html', {'event_id': event_id})

@login_required(login_url="/accounts/login/")
def tables(request):
    context = {
        'parent': 'pages',
        'segment': 'tables'
    }
    return render(request, 'pages/tables.html', context)

@login_required(login_url="/accounts/login/")
def billing(request):
    context = {
        'parent': 'pages',
        'segment': 'billing'
    }
    return render(request, 'pages/billing.html', context)

@login_required(login_url="/accounts/login/")
def vr(request):
    context = {
        'parent': 'pages',
        'segment': 'vr'
    }
    return render(request, 'pages/virtual-reality.html', context)

@login_required(login_url="/accounts/login/")
def rtl(request):
    context = {
        'parent': 'pages',
        'segment': 'rtl'
    }
    return render(request, 'pages/rtl.html', context)

@login_required(login_url="/accounts/login/")
def profile(request):
    context = {
        'parent': 'pages',
        'segment': 'profile'
    }
    return render(request, 'pages/profile.html', context)

# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/sign-in.html'
  form_class = LoginForm

class UserRegistration(CreateView):
   template_name = 'accounts/sign-up.html'
   form_class = RegistrationForm
   success_url = "/accounts/login/"

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm

