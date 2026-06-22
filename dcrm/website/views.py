from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Station
import re

def home(request):
    if request.user.is_authenticated:
        if request.user.rol == 'administrador':
            return redirect('admin_dashboard')
        else:
            return redirect('passenger_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messages.error(request, "Formato de correo inválido.")
            return redirect('home')

        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            if not user.is_active:
                messages.error(request, "Tu cuenta está inactiva.")
                return redirect('home')
            
            login(request, user)
            if user.rol == 'administrador':
                return redirect('admin_dashboard')
            else:
                return redirect('passenger_dashboard')
        else:
            messages.error(request, "Credenciales incorrectas")
            return redirect('home')
            
    return render(request, 'login.html', {})

def register_user(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        rol = request.POST.get('rol', 'usuario')
        
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            messages.error(request, "El nombre solo puede contener letras y espacios.")
            return redirect('register')
            
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messages.error(request, "Formato de correo inválido.")
            return redirect('register')
            
        if not re.match(r"^[a-zA-Z0-9!@#\$%\^\&*\)\(+=._-]{8,}$", password):
            messages.error(request, "La contraseña no cumple con los requisitos de seguridad.")
            return redirect('register')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('register')
            
        username = email.split('@')[0]
        if CustomUser.objects.filter(username=username).exists():
            username = f"{username}_{CustomUser.objects.count()}"

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombre,
            rol=rol
        )
        login(request, user)
        messages.success(request, "Usuario registrado exitosamente")
        return redirect('passenger_dashboard')
        
    return render(request, 'register.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def admin_dashboard(request):
    if request.user.rol != 'administrador':
        return redirect('passenger_dashboard')
        
    users = CustomUser.objects.all().order_by('id')
    return render(request, 'admin_dashboard.html', {'users': users})

@login_required
def toggle_user_status(request, user_id):
    if request.user.rol != 'administrador':
        return redirect('home')
    
    user = get_object_or_404(CustomUser, id=user_id)
    if user.id != request.user.id:  # Can't disable oneself
        user.is_active = not user.is_active
        user.save()
    return redirect('admin_dashboard')

@login_required
def passenger_dashboard(request):
    if request.user.rol == 'administrador':
        return redirect('admin_dashboard')
        
    stations = Station.objects.all()
    return render(request, 'passenger_dashboard.html', {'stations': stations})

@login_required
def edit_user(request, user_id):
    if request.user.rol != 'administrador':
        return redirect('home')
        
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('nombre')
        user.email = request.POST.get('email')
        rol = request.POST.get('rol')

        if rol in ['administrador', 'usuario'] and user.id != request.user.id:
            user.rol = rol
            
        user.save()
        messages.success(request, f"Datos de {user.first_name} actualizados.")
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

from .models import Report, GlobalNotification

@login_required
def api_reports(request):
    if request.user.rol != 'administrador':
        return redirect('home')
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'partials/reports_list.html', {'reports': reports})

@login_required
def api_notifications(request):
    if request.user.rol != 'administrador':
        return redirect('home')
    notifications = GlobalNotification.objects.all().order_by('-created_at')
    return render(request, 'partials/notifications_list.html', {'notifications': notifications})
