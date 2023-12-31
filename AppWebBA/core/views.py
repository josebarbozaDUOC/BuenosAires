from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, PerfilUsuario, SolicitudServicio, Factura, GuiaDespacho
from .forms import ProductoForm, IniciarSesionForm
from .forms import RegistrarUsuarioForm, PerfilUsuarioForm, SolicitudServicioForm
#from .error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.db import connection
import random
import requests
import datetime
from datetime import datetime

def home(request):
    return render(request, "core/home.html")

def iniciar_sesion(request):
    data = {"mesg": "", "form": IniciarSesionForm()}

    if request.method == "POST":
        form = IniciarSesionForm(request.POST)
        if form.is_valid:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(home)
                else:
                    data["mesg"] = "¡La cuenta o la password no son correctos!"
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, "core/iniciar_sesion.html", data)

def cerrar_sesion(request):
    logout(request)
    return redirect(home)

def tienda(request):

    if request.method == 'GET':
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("EXEC SP_OBTENER_STOCK")

        # Obtener los resultados
        results = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        data = []
        for row in results:
            idstock = row[0]
            idprod = row[1]
            nomprod = row[2]
            descprod = row[3]
            precio = row[4]
            imagen = row[5]
            nrofac = row[6]
            estado = row[7]

            data.append({
                'idstock': idstock,
                'idprod': idprod,
                'nomprod': nomprod,
                'descprod': descprod,
                'precio' : precio,
                'imagen' : imagen,
                'nrofac': nrofac,
                'estado': estado
            })

        data = {'lista': data }

        return render(request, "core/tienda.html", data)


#https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
#https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
#https://www.transbankdevelopers.cl/referencia/webpay

# Tipo de tarjeta   Detalle                        Resultado
#----------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)

@csrf_exempt
def ficha(request, id):

    # Cuando el usuario hace clic en el boton COMPRAR, se ejecuta el METODO POST del
    # formulario de ficha.html, con lo cual se redirecciona la página para que
    # llegue a esta VISTA llamada "FICHA". A continuacion se verifica que sea un POST 
    # y se valida que se trate de un usuario autenticado que no sea de estaff, 
    # es decir, se comprueba que la compra sea realizada por un CLIENTE REGISTRADO.
    # Si se tata de un CLIENTE REGISTRADO, se redirecciona a la vista "iniciar_pago"
    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            
            return redirect(iniciar_pago, int(id))
        else:
            # Si el usuario que hace la compra no ha iniciado sesión,
            # entonces se le envía un mensaje en la pagina para indicarle
            # que primero debe iniciar sesion antes de comprar
            data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"
    

    precio_usd = obtener_valor_usd()
    amount = Producto.objects.get(idprod=id).precio
    conv_usd = precio_usd * amount
    print(conv_usd)
    data = {"mesg": "", "producto": None, 'conv_usd': conv_usd}

    # Si visitamos la URL de FICHA y la pagina no nos envia un METODO POST, 
    # quiere decir que solo debemos fabricar la pagina y devolvera al browser
    # para que se muestren los datos de la FICHA
    data["producto"] = Producto.objects.get(idprod=id)
    return render(request, "core/ficha.html", data)

@csrf_exempt
def iniciar_pago(request, id):

    # Esta es la implementacion de la VISTA iniciar_pago, que tiene la responsabilidad
    # de iniciar el pago, por medio de WebPay. Lo primero que hace es seleccionar un 
    # número de orden de compra, para poder así, identificar a la propia compra.
    # Como esta tienda no maneja, en realidad no tiene el concepto de "orden de compra"
    # pero se indica igual
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username

    if (int(id) > int(0)):
        amount = Producto.objects.get(idprod=id).precio
    else:
        amount=25000
        
    return_url = 'http://127.0.0.1:8000/pago_exitoso/'+ id

    # response = Transaction.create(buy_order, session_id, amount, return_url)
    commercecode = "597055555532"
    apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

    tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
    response = tx.create(buy_order, session_id, amount, return_url)
    print(response['token'])

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()
    if request.user.is_authenticated:
        
        tipousuario = PerfilUsuario.objects.get(user_id=request.user.id).tipousu

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "dirusu": perfil.dirusu,
        'tipousu' : tipousuario
    }

    return render(request, "core/iniciar_pago.html", context)

@csrf_exempt
def pago_exitoso(request, id):

    if request.method == "GET":
        token = request.GET.get("token_ws")
        print("commit for token_ws: {}".format(token))
        commercecode = "597055555532"
        apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.commit(token=token)
        print("response: {}".format(response))

        user = User.objects.get(username=response['session_id'])
        perfil = PerfilUsuario.objects.get(user=user)

        context = {
            "buy_order": response['buy_order'],
            "session_id": response['session_id'],
            "amount": response['amount'],
            "response": response,
            "token_ws": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "rut": perfil.rut,
            "dirusu": perfil.dirusu,
            "response_code": response['response_code']
        }                 

        #4051885600446623
        # Se guarda en DB usando el procedimiento almacenado SP_COMPRA
        cursor = connection.cursor()
        if (int(id) > int(0)):
            cursor.execute(
                "EXEC SP_COMPRA @nrofac=%s, @rutcli=%s, @idprod=%s, @descfac=%s, @monto=%s, @nrogd=%s, @nrosol=%s, @tiposol=%s, @fechavisita=%s, @ruttec=%s, @descsol=%s",
                [0, perfil.rut, id, '', response['amount'], 0, 0, 'Instalación', '', '', ''])
        else:
            tiposol     = request.session.get('tiposol')
            fechavisita = request.session.get('fechavisita')
            descsol     = request.session.get('descsol')

            cursor.execute(
                "EXEC SP_COMPRA @nrofac=%s, @rutcli=%s, @idprod=%s, @descfac=%s, @monto=%s, @nrogd=%s, @nrosol=%s, @tiposol=%s, @fechavisita=%s, @ruttec=%s, @descsol=%s",
                [0, perfil.rut, None, tiposol, 25000, 0, 0, tiposol, fechavisita, '', descsol])

        return render(request, "core/pago_exitoso.html", context)
    else:
        return redirect(home)

@csrf_exempt
def administrar_productos(request, action, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(home)

    data = {"mesg": "", "form": ProductoForm, "action": action, "id": id, "formsesion": IniciarSesionForm}

    if action == 'ins':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos vehículos con el mismo ID!"

    elif action == 'upd':
        objeto = Producto.objects.get(idprod=id)
        if request.method == "POST":
            form = ProductoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El producto fue actualizado correctamente!"
        data["form"] = ProductoForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(idprod=id).delete()
            data["mesg"] = "¡El producto fue eliminado correctamente!"
            return redirect(administrar_productos, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El producto ya estaba eliminado!"

    data["list"] = Producto.objects.all().order_by('idprod')
    return render(request, "core/administrar_productos.html", data)

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            tipousu = "Cliente"
            dirusu = request.POST.get("dirusu")
            PerfilUsuario.objects.update_or_create(user=user, rut=rut, tipousu=tipousu, dirusu=dirusu)
            return redirect(iniciar_sesion)
    form = RegistrarUsuarioForm()
    return render(request, "core/registrar_usuario.html", context={'form': form})

def perfil_usuario(request):
    data = {"mesg": "", "form": PerfilUsuarioForm}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            perfil = PerfilUsuario.objects.get(user=user)
            perfil.rut = request.POST.get("rut")
            perfil.tipousu = request.POST.get("tipousu")
            perfil.dirusu = request.POST.get("dirusu")
            perfil.save()
            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name
    form.fields['email'].initial = request.user.email
    form.fields['rut'].initial = perfil.rut
    form.fields['tipousu'].initial = perfil.tipousu
    form.fields['dirusu'].initial = perfil.dirusu
    data["form"] = form
    return render(request, "core/perfil_usuario.html", data)

def obtener_solicitudes_de_servicio(request):

    rut = PerfilUsuario.objects.get(user=request.user).rut
    
    tipous = PerfilUsuario.objects.get(user=request.user).tipousu

    if request.method == 'GET':
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute(f"EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO '{tipous}', '{rut}'")

        # Obtener los resultados
        results = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        solicitudes_de_servicio = []
        for row in results:
            solicitudes_de_servicio.append({
                'nrosol': row[0],
                'nomcli': row[1],
                'tiposol': row[2],
                'fechavisita': row[3],
                'hora': row[4],
                'nomtec': row[5],
                'descser': row[6],
                'estadosol': row[7]
            })


        data = {'lista': solicitudes_de_servicio }

        return render(request, "core/obtener_solicitudes_de_servicio.html", data)
    
    
    
def obtener_valor_usd():
    url = 'https://api.exchangerate-api.com/v4/latest/CLP'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            valor_usd = datos['rates']['USD']
            return valor_usd
    except:
        pass
    return 0


def solicitudservicios(request, action, id):
    data = {"mesg": "", "form": SolicitudServicioForm, "action": action, "nrosol": id}

    if request.method == "POST":
        form = SolicitudServicioForm(request.POST, request.FILES)
        if form.is_valid():
            tiposol     = form.cleaned_data['tiposol']
            fechavisita = form.cleaned_data['fechavisita']
            descsol     = form.cleaned_data['descsol']
            fechavisita_str = fechavisita.isoformat()
            request.session['tiposol']      = tiposol
            request.session['fechavisita'] = fechavisita_str
            request.session['descsol']      = descsol

            if request.user.is_authenticated and not request.user.is_staff:
                return redirect(iniciar_pago, 0)
            else: data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"
                  
    
    if action == 'ins':
        if request.method == "POST":
            
            form = SolicitudServicioForm(request.POST, request.FILES)
            
            if form.is_valid:
                try:
                    form.save()                  
                    
                    data["mesg"] = "¡La solicitud fue creada correctamente!"
                except:
                    data["mesg"] = "¡No se puede ingresar una solicitud con una id ya registrada!"
                    

    elif action == 'upd':
        objeto = SolicitudServicio.objects.get(nrosol=id)
        if request.method == "POST":
            form = SolicitudServicioForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El producto fue actualizado correctamente!"
        data["form"] = SolicitudServicioForm(instance=objeto)

    elif action == 'del':
        try:
            SolicitudServicio.objects.get(nrosol=id).delete()
            data["mesg"] = "Â¡El producto fue eliminado correctamente!"
            return redirect(solicitudservicios, action='ins', id = '-1')
        except:
            data["mesg"] = "¡La solicitud ya fue eliminada!"
    

    data["list"] = SolicitudServicio.objects.all().order_by('nrosol')
    return render(request, "core/ingresarsolicitud.html", data)


def obtener_facturas(request):

    rut = PerfilUsuario.objects.get(user=request.user).rut
    
    tipous = PerfilUsuario.objects.get(user=request.user).tipousu

    if request.method == 'GET':
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute(f"EXEC SP_OBTENER_FACTURAS '{tipous}', '{rut}'")

        # Obtener los resultados
        results = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        historialcompras = []
        for row in results:
            historialcompras.append({
                'nrofac': row[0],
                'fechafac': row[1],
                'descfac': row[2],
                'monto': row[3],
                'idprod': row[4],
                'rutcli': row[5]
            })


        data = {'lista': historialcompras }

        return render(request, "core/historialcompras.html", data)



