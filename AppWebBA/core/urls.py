from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import home, administrar_productos, tienda, ficha
from .views import iniciar_sesion, registrar_usuario, cerrar_sesion
from .views import perfil_usuario, iniciar_pago, pago_exitoso, obtener_solicitudes_de_servicio, solicitudservicios, obtener_facturas

urlpatterns = [
    path('', home, name="home"),
    path('tienda', tienda, name="tienda"),
    path('administrar_productos/<action>/<id>', administrar_productos, name="administrar_productos"),
    path('ficha/<id>', ficha, name="ficha"),
    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    path('password_cambiada/', TemplateView.as_view(template_name='core/password_cambiada.html'), name='password_cambiada'),
    path('cambiar_password/', auth_views.PasswordChangeView.as_view(template_name='core/cambiar_password.html', success_url='/password_cambiada'), name='cambiar_password'),
    path('perfil_usuario/', perfil_usuario, name="perfil_usuario"),
    path('iniciar_pago/<id>', iniciar_pago, name="iniciar_pago"),
    path('pago_exitoso/<id>', pago_exitoso, name="pago_exitoso"),
    path('obtener_solicitudes_de_servicio/', obtener_solicitudes_de_servicio, name="obtener_solicitudes_de_servicio"),
    path('solicitudservicio/<action>/<id>', solicitudservicios, name="solicitudservicio"),
    path('obtener_facturas', obtener_facturas, name="obtener_facturas"), 

]