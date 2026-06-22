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

- **Patrón MVC/MVT:** Separación clara entre modelos (`models.py`), lógica de control (`views.py`) y presentación (`templates/`).
- **Principio DRY (Don't Repeat Yourself):** Reutilización de plantillas base (`base.html`), herencia de plantillas (`{% extends %}`) y uso de bucles (`{% for %}`) para evitar la duplicación de código en la UI.
- **Principios SOLID aplicados:**
  - **S (Single Responsibility):** Cada función en `views.py` tiene una única responsabilidad (ej. `api_reports` solo carga reportes).
  - **O (Open/Closed):** Modelos diseñados para ser extendidos sin modificar su núcleo (ej. herencia de `AbstractUser`).

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
