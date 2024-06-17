# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 19:51:18 2022

@author: harol
"""
import os
from getpass import getuser

#%%  Rutas de consulta
current_file = os.path.realpath(__file__)  # Obtener la ruta del archivo actual
ruta_base = os.path.dirname(current_file)
ruta_descargas=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')

# ruta_hoja_estilo=os.path.join(ruta_base, r'UI\Hoja_Estilo\style.css')

ruta_dir_trusted=os.path.join(ruta_base, r'Data')
ruta_trusted=os.path.join(ruta_base, r'Data\trusted.csv')

# ruta_dir_trusted=r"C:\Users\harol\Universidad EAFIT\Proyecto Integrador 1 - Documentos\inspector_datalake\trusted\2024_05"
# ruta_trusted=r"C:\Users\harol\Universidad EAFIT\Proyecto Integrador 1 - Documentos\inspector_datalake\trusted\2024_05\trusted.csv"
