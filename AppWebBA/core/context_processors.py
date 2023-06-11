from .models import PerfilUsuario
from django.shortcuts import render

def tipousu(request):
    if request.user.is_authenticated:
        return {'tipousu': PerfilUsuario.objects.get(user_id=request.user.id).tipousu}
    else:
        return {'tipousu' : 'Anonimo'}