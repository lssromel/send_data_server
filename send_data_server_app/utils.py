import hashlib
import ConfigParser
from import_file import import_file

def handle_uploaded_file(f,name,tmp_dir):

    ruta = tmp_dir + name
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

