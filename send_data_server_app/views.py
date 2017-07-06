# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from utils import handle_uploaded_file
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
import hashlib
from utils import *
from django.core.files import File
import ConfigParser
import os
import urllib2

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
    Config = ConfigParser.ConfigParser()
    Config.read("/workspace/send_data_server/ConfigFile.ini")
    username = request.user.username
    d_entrada = Config.get("clientes",username)
    ip = Config.get("Mongo","ip")
    port = Config.get("Mongo","port")
    archivo = request.data['file']
    name = request.data['name']
    tmp= archivo
    MD5= request.data["MD5"] 
    if MD5_Check(tmp,MD5):
	print "Archivo Cargado al servidor con exito"
        myfile = File(archivo)
        ruta = handle_uploaded_file(myfile,archivo.name)
	code,df=limpieza(d_entrada,ruta,name)
	if code ==0:
	    return HttpResponse(df)
	print "Archivo preprocesado listo"
	if insert_send_data(ip,port,name,username,df):
    	    if os.path.isfile(ruta):
        	os.remove(ruta)
    	    if os.path.isfile(ruta[:-4]):
        	os.remove(ruta[:-4])
	    urllib2.urlopen("http://127.0.0.1:5005/inicio_tarea/")
	    return HttpResponse("Archivo escrito en la base de Datos")
            

    else:
	return HttpResponse("Los md5 no coinciden")


