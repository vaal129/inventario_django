# MetroMed - Sistema de Gestión y Administración

MetroMed es una aplicación web desarrollada en **Django** utilizando el patrón de arquitectura **MVT** (Modelo-Vista-Template), que se corresponde estrechamente con el MVC (Modelo-Vista-Controlador).

Este proyecto cumple con los requerimientos del módulo de "Soporte y Administración" implementando las especificaciones para el **Entregable Final**.

## 🎨 Paleta de Colores y Diseño
Se ha implementado una paleta basada en tonos **Violeta** según las especificaciones.
- Color principal: `#1a0b2e`
- Color de acento: `#b026ff`

Se ha integrado **Bootstrap Local** sin dependencias de CDNs externas.

## 🚀 Funcionalidades Principales

### 1. Login con Roles y CRUD Completo
- **Roles:** El sistema soporta los roles de `administrador` y `usuario`.
- **CRUD:** El panel de administrador permite realizar operaciones de creación, lectura, actualización y desactivación de usuarios (borrado lógico).

### 2. Módulo de Soporte y Administración (SPA)
El panel de administración funciona como una **Single Page Application (SPA)**, permitiendo navegar entre las siguientes secciones sin recargar la página:
- **Gestión de Usuarios:** Ver, crear y editar usuarios.
- **Reportes (RF-33 a RF-36):** Los administradores pueden visualizar el historial de reportes o sugerencias registrados, con validación de estado.
- **Notificaciones Globales (RF-37 a RF-39):** Los administradores pueden enviar notificaciones globales visibles.

## 🔒 4 Capas de Seguridad Implementadas

El sistema aplica seguridad rigurosa mediante 4 capas:
1. **Capa 1: Autenticación de Usuario (Django Auth):** Solo usuarios autenticados mediante el sistema nativo de Django pueden acceder a los paneles (`@login_required`).
2. **Capa 2: Autorización Basada en Roles:** Verificación a nivel de vista que comprueba si el usuario actual tiene el `rol == 'administrador'` antes de permitir la ejecución de lógica administrativa.
3. **Capa 3: Validación de Entradas (Regex Backend/Frontend):** Uso de expresiones regulares estrictas (ej. `^[a-zA-Z0-9!@#\$%\^\&*\)\(+=._-]{8,}$` para contraseñas) tanto en HTML5 `pattern` como en `views.py` (librería `re`), evitan ataques de inyección y aseguran datos limpios.
4. **Capa 4: Protección contra Falsificación de Peticiones (CSRF):** Uso obligatorio del token `{% csrf_token %}` en todos los formularios POST, validado internamente por el Middleware de Django.

## 📐 Patrones de Diseño y Principios

- **Patrón Arquitectónico MVT (Model-View-Template):** Adaptación del clásico MVC. Separa la lógica de base de datos (`models.py`), la lógica de negocio (`views.py`) y la presentación visual (`templates/`).
- **Patrón Active Record:** Presente en el ORM de Django. Los modelos (`CustomUser`, `Report`, `GlobalNotification`) envuelven una fila de la base de datos e incluyen la lógica de persistencia.
- **Patrón Decorator (Decorador):** Utilizado explícitamente en `views.py` (`@login_required`) para extender el comportamiento de "verificación de sesión" sin alterar la función interna.
- **Patrón Template Method (Método Plantilla):** Aplicado en las plantillas HTML (herencia). El `base.html` define el esqueleto principal y deja bloques (`{% block content %}`) para que las vistas hijas lo rellenen.
- **Patrón Front Controller (Controlador Frontal):** En Django, `urls.py` recibe todas las peticiones web y actúa como un controlador centralizado que delega a la vista correspondiente.
- **Patrón Repository / DAO (Data Access Object):** Utilizado a través del "Manager" de Django. El objeto `.objects` (ej: `Report.objects.filter()`) abstrae las consultas SQL y actúa como repositorio.
- **Patrón Factory Method (Método Fábrica):** Utilizado al instanciar usuarios (`CustomUser.objects.create_user()`) para delegar el proceso complejo de empaquetado y encriptación de contraseñas.
- **Patrón Singleton:** Usado internamente por Django para gestionar la conexión a la base de datos (MySQL) y las configuraciones globales (`settings.py`), garantizando una única instancia en ejecución.
- **Patrón Strategy (Estrategia):** Aplicado por el sistema de autenticación de contraseñas de Django, permitiendo cambiar dinámicamente el algoritmo de hashing (PBKDF2) sin afectar la lógica de login.
- **Patrón Observer (Observador / Señales):** Presente a través de las *Signals* de Django, que permiten notificar de forma desacoplada a diferentes partes del sistema cuando ocurre un evento (como el registro de un objeto en BD).

### Principios de Programación
- **Principio DRY (Don't Repeat Yourself):** Reutilización de plantillas base (`base.html`), herencia de plantillas (`{% extends %}`) y uso de bucles (`{% for %}`) para evitar la duplicación de código en la UI.
- **Principios SOLID aplicados:**
  - **S (Single Responsibility):** Cada función en `views.py` tiene una única responsabilidad.
  - **O (Open/Closed):** Modelos diseñados para ser extendidos sin modificar su núcleo.

## 🛠️ Instalación y Ejecución

1. Clona este repositorio.
2. Instala los requerimientos:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta las migraciones:
   ```bash
   python manage.py migrate
   ```
4. Levanta el servidor:
   ```bash
   python manage.py runserver
   ```
