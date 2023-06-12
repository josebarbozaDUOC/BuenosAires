from django.urls import path
from django.contrib import admin
from .views import producto_create, producto_read, producto_read_all
from .views import producto_update, producto_delete, login, obtener_equipos_en_bodega, obtener_productos\
    ,verificar_password, obtener_equipos_anwo, obtener_guias_de_despacho, reservar_equipo_anwo\
    ,obtener_stock, obtener_facturas ,validar_login_escritorio, modificar_estado_guia_de_despacho

urlpatterns = [
    path('producto_create/', producto_create.as_view(), name="producto_create"),
    path('producto_update/', producto_update.as_view(), name="producto_update"),
    path('producto_read/<id>/', producto_read, name="producto_read"),
    path('producto_read_all/', producto_read_all, name='producto_read_all'),
    path('producto_delete/<id>/', producto_delete, name="producto_delete"),
    path('login', login, name='login'),
    path('obtener_productos', obtener_productos, name='obtener_productos'),
    path('verificar_password/<username>/<password>', verificar_password, name="verificar_password"),

    path('validar_login_escritorio/<username>/<password>/<tipousu>', validar_login_escritorio, name="validar_login_escritorio"),

    path('obtener_equipos_en_bodega', obtener_equipos_en_bodega, name='obtener_equipos_en_bodega'),
    path('obtener_guias_de_despacho', obtener_guias_de_despacho, name='obtener_guias_de_despacho'),
    path('modificar_estado_guia_de_despacho/<nro>/<estado>', modificar_estado_guia_de_despacho, name='modificar_estado_guia_de_despacho'),
    
    path('obtener_equipos_anwo', obtener_equipos_anwo, name='obtener_equipos_anwo'),
    path('reservar_equipo_anwo/<nroserie>', reservar_equipo_anwo, name='reservar_equipo_anwo'),

    path('obtener_stock', obtener_stock, name='obtener_stock'),
    path('obtener_facturas/<tipousu>/<rut>', obtener_facturas, name='obtener_facturas'),
]
