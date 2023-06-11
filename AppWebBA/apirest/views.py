import re
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators import csrf
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import Producto, PerfilUsuario
from .serializers import ProductoSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

class producto_create(APIView):
    def post(self, request, format=None):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class producto_update(APIView):
    def put(self, request, format=None):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def producto_read(request, id):
    if request.method == 'GET':
        objeto = get_object_or_404(Producto, idprod=id)
        serializer = ProductoSerializer(objeto)
        return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def producto_read_all(request):
    if request.method == 'POST':
        list = Producto.objects.all()
        serializer = ProductoSerializer(list, many=True)
        return Response(serializer.data)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def producto_delete(request, id):
    if request.method == 'DELETE':
        try:
            Producto.objects.get(idprod=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Producto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login(request):
    data = JSONParser().parse(request)
    username = data['username']
    password = data['password']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Usuario inválido")
    password_valida = check_password(password, user.password)
    if not password_valida:
        return Response("Contraseña incorrecta")
    token, created = Token.objects.get_or_create(user=user)
    print(f"Este es el token creado: '{token.key}'")
    return Response(token.key)


@csrf_exempt
@api_view(['GET'])
def obtener_equipos_en_bodega(request):
    if request.method == 'GET':
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("EXEC SP_OBTENER_EQUIPOS_EN_BODEGA")

        # Obtener los resultados
        results = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        data = []
        for row in results:
            idstock = row[0]
            idprod = row[1]
            nomprod = row[2]
            nrofac = row[3]
            estado = row[4]

            data.append({
                'idstock': idstock,
                'idprod': idprod,
                'nomprod': nomprod,
                'nrofac': nrofac,
                'estado': estado
            })

        # Devolver los datos como respuesta JSON
        return JsonResponse(data, safe=False)

@csrf_exempt
@api_view(['GET'])
def obtener_productos(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_OBTENER_PRODUCTOS")
        results = cursor.fetchall()
        data = []
        for row in results:
            idprod = row[0]
            nomprod = row[1]
            descprod = row[2]
            precio = row[3]
            imagen = row[4]
            data.append({
                'idprod': idprod,
                'nomprod': nomprod,
                'descprod': descprod,
                'precio': precio,
                'imagen': imagen
            })

        # Devolver los datos como respuesta JSON
        return JsonResponse(data, safe=False)

#obtener_equipos_anwo
@csrf_exempt
@api_view(['GET'])
def obtener_equipos_anwo(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_OBTENER_EQUIPOS_ANWO")
        results = cursor.fetchall()
        data = []
        for row in results:
            nroserie = row[0]
            producto = row[1]
            precio = row[2]
            reservado = row[3]
            data.append({
                'nroserie': nroserie,
                'producto': producto,
                'precio': precio,
                'reservado': reservado
            })
        return JsonResponse(data, safe=False)
    
#obtener_guias_de_despacho
@csrf_exempt
@api_view(['GET'])
def obtener_guias_de_despacho(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_OBTENER_GUIAS_DE_DESPACHO")
        results = cursor.fetchall()
        data = []
        for row in results:
            nrogd = row[0]
            producto = row[1]
            fechagd = row[2]
            estadogd = row[3]
            nrofac = row[4]
            cliente = row[5]
            data.append({
                'nrogd': nrogd,
                'producto': producto,
                'fechagd': fechagd,
                'estadogd': estadogd,
                'nrofac': nrofac,
                'cliente': cliente
            })
        return JsonResponse(data, safe=False)
    
    
#reservar_equipo_anwo
@csrf_exempt
@api_view(['PUT'])
def reservar_equipo_anwo(request, nroserie):
    if request.method == 'PUT':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_RESERVAR_EQUIPO_ANWO %s", (nroserie,))
        return JsonResponse({'message': 'Equipo actualizado correctamente.'})
    
#estado_despachado_guia_de_despacho
@csrf_exempt
@api_view(['PUT'])
def estado_despachado_guia_de_despacho(request, nro):
    if request.method == 'PUT':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_ESTADO_DESPACHADO_GUIA_DE_DESPACHO %s", (nro,))
        return JsonResponse({'message': 'Guía de Despacho actualizada correctamente.'})
    
#estado_entregado_guia_de_despacho
@csrf_exempt
@api_view(['PUT'])
def estado_entregado_guia_de_despacho(request, nro):
    if request.method == 'PUT':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_ESTADO_ENTREGADO_GUIA_DE_DESPACHO %s", (nro,))
        return JsonResponse({'message': 'Guía de Despacho actualizada correctamente.'})
      
@csrf_exempt
@api_view(['GET'])
def verificar_password(request, username, password):
    if request.method == 'GET':
        user = authenticate(username=username, password=password)
        respuesta = { 'autenticado': user is not None }
        return JsonResponse(respuesta, safe=False)
    
@csrf_exempt
@api_view(['GET'])
def validar_login_escritorio(request, username, password, tipousu):
    if request.method == 'GET':
        user = authenticate(username=username, password=password)
        if user is not None:
            perfil = PerfilUsuario.objects.filter(user=user, tipousu=tipousu).exists()
            perfil_adm = PerfilUsuario.objects.filter(user=user, tipousu='Administrador').exists()
            respuesta = {'autenticado': perfil or perfil_adm}
        else:
            respuesta = {'autenticado': False}
        return JsonResponse(respuesta, safe=False)
    
#SP gonzalo: en view 
@csrf_exempt
@api_view(['GET'])
def obtener_stock(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_OBTENER_STOCK")
        results = cursor.fetchall()
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
        return JsonResponse(data, safe=False)
    
@csrf_exempt
@api_view(['GET'])
def obtener_facturas(request, tipousu, rut):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_OBTENER_FACTURAS %s %s", (tipousu, rut,))
        results = cursor.fetchall()
        data = []
        for row in results:
            nrofac = row[0]
            fechafac = row[1]
            descfac = row[2]
            monto = row[3]
            idprod = row[4]
            rutcli = row[5]
            data.append({
                'nrofac': nrofac,
                'fechafac': fechafac,
                'descfac': descfac,
                'monto': monto,
                'idprod' : idprod,
                'rutcli' : rutcli,
            })
        return JsonResponse(data, safe=False)