#%%
import os
import datetime as dt
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem

#%% Funciones
def leer_y_analizar_csv_files(folder_path) ->pd.DataFrame:     ##
    data = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            mod_time = os.path.getmtime(file_path)
            mod_time = dt.datetime.fromtimestamp(mod_time)
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            ultima_date = df.index.max()
            data.append({ 'Nombre del Archivo': filename, 
                'Fecha de Modificación': mod_time, 
                'Última Fecha en el Índice': ultima_date})
            
    df_info_df = pd.DataFrame(data)   
    return df_info_df

def cargar_tab(df, table_widget):               ## Función para cargar una dataframe en una tabletwidget
    table_widget.setRowCount(df.shape[0])
    table_widget.setColumnCount(df.shape[1])
    table_widget.setHorizontalHeaderLabels(df.columns)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))