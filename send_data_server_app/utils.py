import hashlib
import ConfigParser
from import_file import import_file
from pymongo import MongoClient
import pymongo 
import json
import datetime
import time


def handle_uploaded_file(f,name):
    Config = ConfigParser.ConfigParser()
    Config.read("/workspace/send_data_server/ConfigFile.ini")
    tmp = Config.get("tmp_dir","directorio")

    ruta = tmp+name
    with open(ruta, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return ruta

def MD5_Check(archivo,MD5_Original):
    MD5_Load =hashlib.md5(archivo.read()).hexdigest()
    if MD5_Load==MD5_Original:
        return True
    else:
	return False

def limpieza(d_entrada,ruta,nombre):
    a=import_file(d_entrada+'/carga_inicial.py')
    code ,df=a.carga_archivo(ruta,nombre)
    return code, df

def insert_send_data(ip,port,name,user,df):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    client = MongoClient(host=(str(ip)+":"+str(port)))
    db = client[user]
    Archivos_Cargados = db.Archivos_Cargados
    Tabla = Archivos_Cargados[name]
    df=df.to_dict("records")
    result = Tabla.insert_many(df).acknowledged
    if result:
        db_time = db["time"]
	tabla_time = db_time[name]
	tabla_time.insert_one({"time":st})
    client.close()
    return result
