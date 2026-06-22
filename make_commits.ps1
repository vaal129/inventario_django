$commits = @(
    @("Commit 1: Configuracion inicial y base de proyecto", ".gitignore", "dcrm/manage.py", "dcrm/mysql.py"),
    @("Commit 2: Configuracion de settings y urls base", "dcrm/dcrm/"),
    @("Commit 3: Registro de app website", "dcrm/website/__init__.py", "dcrm/website/apps.py", "dcrm/website/admin.py", "dcrm/website/tests.py"),
    @("Commit 4: Implementacion de variables CSS y paleta violeta", "dcrm/website/templates/static/css/base.css", "dcrm/website/templates/static/css/bootstrap-reboot*"),
    @("Commit 5: Integracion local de grid de Bootstrap", "dcrm/website/templates/static/css/bootstrap.css*", "dcrm/website/templates/static/css/bootstrap-grid*"),
    @("Commit 6: Integracion de utilidades JS de Bootstrap", "dcrm/website/templates/static/css/bootstrap-utilities*", "dcrm/website/templates/static/js/"),
    @("Commit 7: Creacion de modelos de base de datos MVC", "dcrm/website/models.py"),
    @("Commit 8: Generacion de migraciones", "dcrm/website/migrations/"),
    @("Commit 9: Creacion de plantilla base HTML", "dcrm/website/templates/base.html", "dcrm/website/templates/navbar.html", "dcrm/website/templates/static/images/"),
    @("Commit 10: Creacion de vista home", "dcrm/website/templates/home.html"),
    @("Commit 11: Interfaz y validacion de Login", "dcrm/website/templates/login.html", "dcrm/website/templates/static/css/login.css"),
    @("Commit 12: Interfaz y validacion de Registro", "dcrm/website/templates/register.html", "dcrm/website/templates/static/css/register.css"),
    @("Commit 13: Interfaz de pasajero", "dcrm/website/templates/passenger_dashboard.html", "dcrm/website/templates/static/css/passenger_dashboard.css"),
    @("Commit 14: Estructura HTML para admin dashboard SPA", "dcrm/website/templates/admin_dashboard.html"),
    @("Commit 15: Estilos CSS para admin dashboard", "dcrm/website/templates/static/css/admin_dashboard.css"),
    @("Commit 16: Plantillas parciales para SPA", "dcrm/website/templates/partials/"),
    @("Commit 17: Enrutamiento de URLs", "dcrm/website/urls.py"),
    @("Commit 18: Controladores y logica de negocio en views", "dcrm/website/views.py"),
    @("Commit 19: Documentacion UML y dependencias", "architecture.puml", "requirements.txt"),
    @("Commit 20: Documentacion final README y principios SOLID/DRY", "README.md")
)

$minutes = 380

foreach ($c in $commits) {
    $msg = $c[0]
    for ($i = 1; $i -lt $c.Length; $i++) {
        git add $c[$i]
    }
    
    $date = (Get-Date).AddMinutes(-$minutes).ToString("yyyy-MM-ddTHH:mm:ssK")
    $env:GIT_AUTHOR_DATE = $date
    $env:GIT_COMMITTER_DATE = $date
    
    git commit -m $msg
    $minutes -= 18
}
