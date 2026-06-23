from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Station, Report, GlobalNotification
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
        confirm_password = request.POST.get('confirm_password', '')
        rol = 'usuario'
        
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            messages.error(request, "El nombre solo puede contener letras y espacios.")
            return redirect('register')
            
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messages.error(request, "Formato de correo inválido.")
            return redirect('register')
            
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
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
    total_reports = Report.objects.filter(status='pendiente').count()
    total_notifs = GlobalNotification.objects.count()
    stations = Station.objects.all().order_by('name')
    return render(request, 'admin_dashboard.html', {
        'users': users,
        'total_reports': total_reports,
        'total_notifs': total_notifs,
        'stations': stations,
    })

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
def delete_user(request, user_id):
    if request.user.rol != 'administrador':
        return redirect('home')
    
    user = get_object_or_404(CustomUser, id=user_id)
    if user.id != request.user.id:
        user.delete()
        messages.success(request, f"Usuario {user.username} eliminado correctamente.")
    else:
        messages.error(request, "No puedes eliminar tu propia cuenta de administrador.")
    return redirect('admin_dashboard')

@login_required
def passenger_dashboard(request):
    if request.user.rol == 'administrador':
        return redirect('admin_dashboard')
        
    stations = Station.objects.all()
    notifications = GlobalNotification.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'passenger_dashboard.html', {'stations': stations, 'notifications': notifications})

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

@login_required
def submit_report(request):
    if request.method == 'POST':
        problem_type = request.POST.get('problem_type')
        description = request.POST.get('description')
        if problem_type and description:
            Report.objects.create(
                user=request.user,
                problem_type=problem_type,
                description=description
            )
            messages.success(request, "¡Tu reporte ha sido enviado con éxito!")
        return redirect('passenger_dashboard' if request.user.rol != 'administrador' else 'admin_dashboard')
    return redirect('home')

@login_required
def update_report_status(request, report_id):
    if request.user.rol != 'administrador':
        return redirect('home')
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pendiente', 'validado', 'descartado']:
            report.status = new_status
            report.save()
            messages.success(request, f"Estado del reporte actualizado a {new_status}")
    return redirect('admin_dashboard')

@login_required
def delete_report(request, report_id):
    if request.user.rol != 'administrador':
        return redirect('home')
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        report.delete()
        messages.success(request, "Reporte descartado exitosamente")
    return redirect('admin_dashboard')

@login_required
def create_notification(request):
    if request.user.rol != 'administrador':
        return redirect('home')
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            GlobalNotification.objects.create(
                message=message,
                created_by=request.user
            )
            messages.success(request, "Notificación global publicada")
    return redirect('admin_dashboard')

@login_required
def toggle_notification(request, notif_id):
    if request.user.rol != 'administrador':
        return redirect('home')
    notif = get_object_or_404(GlobalNotification, id=notif_id)
    if request.method == 'POST':
        notif.is_active = not notif.is_active
        notif.save()
        status = "activada" if notif.is_active else "desactivada"
        messages.success(request, f"Notificación {status} exitosamente")
    return redirect('admin_dashboard')

@login_required
def delete_notification(request, notif_id):
    if request.user.rol != 'administrador':
        return redirect('home')
    notif = get_object_or_404(GlobalNotification, id=notif_id)
    if request.method == 'POST':
        notif.delete()
        messages.success(request, "Notificación eliminada exitosamente")
    return redirect('admin_dashboard')

@login_required
def toggle_station(request, station_id):
    if request.user.rol != 'administrador':
        return redirect('home')
    station = get_object_or_404(Station, id=station_id)
    if request.method == 'POST':
        station.is_active = not station.is_active
        station.save()
        estado = 'activada' if station.is_active else 'desactivada'
        messages.success(request, f"Estación {station.name} {estado} exitosamente.")
    return redirect('admin_dashboard')
