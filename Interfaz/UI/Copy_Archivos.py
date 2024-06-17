# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:44:39 2023

@author: 1017225910
"""
#%% Archivos Ui
import shutil
import subprocess
import os
from datetime import datetime

current_file = os.path.realpath(__file__)  # Obtener la ruta del archivo actual
ruta_base = os.path.dirname(current_file)


fuente_base=ruta_base
destino=ruta_base

Archivos_ui = {'Interfaz_IdentificacionFallas':'Interfaz_Principal',
            }

def TiempoModificacion(ruta):
    info_archivo = os.stat(ruta)
    fecha_modificacion = info_archivo.st_mtime
    fecha_actual = datetime.now()
    diferencia_segundos = (fecha_actual - datetime.fromtimestamp(fecha_modificacion)).total_seconds()
    return diferencia_segundos


#%% Convirtiendo todos los archivos a .py

# ACTUALIZA LAS ULTIMAS 12 HORAS
for key in Archivos_ui.keys():
    ruta=fuente_base+r'\\'+key+r'.ui'
    if TiempoModificacion(ruta)<3600*12:
        command = f"pyuic5 {key}.ui -o {Archivos_ui[key]}.py"
        subprocess.run(command, shell=True)
        print(key)
        # Fuente = fuente_base+r'\\'+Archivos_ui[key]+r'.py'
        # try:
        #     shutil.copy(Fuente, destino,follow_symlinks=True)
        # except:
        #     pass

# %%
