# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
import hashlib
from utils import *

import ConfigParser
import os

# Create your views here.

@api_view(['POST'])
def login_user(request):
    username = request.POST.get("username", False)
    password = request.POST.get("password", False)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("Logged In")
    else:
        return HttpResponse("No Logged")

@login_required
def logout_user(request):
    logout(request)
    return HttpResponse("Logout Ok")

@login_required
@api_view(['POST'])
def send_data(request):

    username = request.user.username
    archivo = request.data['file']
    name = request.data['name']
    MD5= request.data["MD5"] 

    Config = ConfigParser.ConfigParser()
    Config.read("/workspace/send_data_server/ConfigFile.ini")
    tmp_dir = Config.get("tmp_dir",username)
    
    tmp = archivo

    if MD5_Check(tmp,MD5):

        myfile = File(archivo)
        ruta = handle_uploaded_file(myfile,archivo.name,tmp_dir)
	HttpResponse("Archivo Cargado en el servidor")
    
    else:
	HttpResponse("Los MD5 no coinciden, reintente enviar el archivo")


