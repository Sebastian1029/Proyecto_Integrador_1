#%% LIBRERIAS
import sys
from UI.Interfaz_Principal import Ui_MainWindow_IdentificacionFallas as Ui_MainWindow
from PyQt5.QtWidgets import QWidget,QVBoxLayout
# from rutas import ruta_hoja_estilo
from PyQt5 import QtWidgets,QtCore

from Funciones.graficar import graficar_2
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio 
pio.renderers.default = "browser"
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler, Normalizer, QuantileTransformer
from tslearn.clustering import TimeSeriesKMeans
from sklearn.metrics import silhouette_score
from Funciones.Decoradores import color_button,color_button2
from Funciones.generales import leer_y_analizar_csv_files,cargar_tab
from Modulos.clase_plotly import Multigrafica
from rutas import ruta_trusted,ruta_dir_trusted

from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QStandardItemModel, QStandardItem
os.environ['QT_MAC_WANTS_LAYER'] = '1'
#%% VENTANA PRINCIPAL
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) #habilita DPI alto, borrar en caso de que produsca error. 

class MiFormulario(QtWidgets.QMainWindow):                              #Verificar que en la clase principal, diga Ui_MainWindow (se pone .QMainWindow) 
    def __init__(self,parent=None):                                     #o Ui_Dialog (se pone .QDialog)
        QtWidgets.QWidget.__init__(self,parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # with open (ruta_hoja_estilo) as file: 
        #     self.setStyleSheet(file.read())
        
        # Conectando botones
        self.ui.pushButton_CargaDatos.clicked.connect(self.acc_info)
        self.ui.pushButton_CargaDatos.clicked.connect(lambda: self.lect_proce())
        self.ui.pushButton_correr_actual.clicked.connect(self.analisis_inicial)
        self.ui.pushButton_escalar.clicked.connect(self.escalar)
        self.ui.pushButton_grafCodo.clicked.connect(self.kmean)
        self.ui.pushButton_graficarcluster.clicked.connect(lambda: self.graficar_cluster(int(self.ui.lineEdit_2.text())))

        # FUNCIONES
    @color_button('ui','pushButton_CargaDatos')
    def acc_info(self):
        df = leer_y_analizar_csv_files(ruta_dir_trusted)
        cargar_tab(df,self.ui.tableWidget)

    def clear_tabs(self, tab_widget):
        while tab_widget.count() > 0:
            tab_widget.removeTab(0)

    def init_plot(self,tabWidget,fig):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        # Generar HTML para incrustar en QWebEngineView
        html = fig.to_html(include_plotlyjs='cdn')

        # Crear y configurar QWebEngineView
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setHtml(html)

        # Agregar QWebEngineView al layout del widget central
        tab_layout.addWidget(self.browser)
        tabWidget.addTab(tab, f"Tab {tabWidget.count() + 1}")

    @color_button('ui','pushButton_CargaDatos')
    def lect_proce(self):

        #% LECTURA Y PROCESAMIENTO INICIAL DE LOS DATOS
        # df=pd.read_csv(ruta_df,parse_dates=[0],index_col=0)

        # df = df[df['COL_KEY'].str.contains('IPv4', case=False)]
        # df.drop(['COL_KEY'],axis=1,inplace=True)
        # df=pd.DataFrame(df[df.index>df.index.max()-pd.Timedelta(hours=168)])
        # df.sort_index(inplace=True)
        # self.df=df

        df = pd.read_csv(ruta_trusted)
        df = df[df['MEDIDA']=='avg']
        df = df[df['DESTINO']=='google.com']
        df = df[~df['DEVICE_NAME'].str.contains('aut-', case=False)]
        df = df[~df['DEVICE_NAME'].str.contains('Claro', case=False)]
        df['FECHA'] = pd.to_datetime(df['FECHA'])################################################################
        prev_week_hour = df['FECHA'].max() - pd.Timedelta(hours=24*3)#######################################
        df = df[df['FECHA'] > prev_week_hour]###########################################################
        df = df[df['COL_KEY'].str.contains('IPv4', case=False)]
        df = df[['FECHA', 'VALOR',
            'DEVICE_NAME']]
        df = df.reset_index(drop = True)
        self.df=df

    @color_button('ui','pushButton_correr_actual')
    def analisis_inicial(self):

        # ANALISIS DE FRECUENCIA
        pivoted_df = self.df.pivot_table(values='VALOR', index='FECHA', columns='DEVICE_NAME', aggfunc='first')
        analyzer =(pivoted_df.count(axis=0) / len(pivoted_df)) * 100
        analyzer2 = analyzer.reset_index()
        analyzer2['rounded_value'] = analyzer2[0].round(1)
        fig = go.Figure(data=[go.Histogram(x=analyzer2['rounded_value'], nbinsx=45)])
        fig.update_layout(title='Histogram of Rounded Values - Eje X porcentaje de datos, Eje Y número de sensores',
            xaxis_title='Porcentaje de datos',
            yaxis_title='Número de sensores')
        self.clear_tabs(self.ui.tabWidget)
        self.init_plot(self.ui.tabWidget,fig)

        # DEJANDO COLUMNAS CON MÁS DEL 30% DE DATOS
        nan_threshold=float(self.ui.lineEdit.text())/100
        print(nan_threshold)
        self.pivoted_df = pivoted_df.loc[:,pivoted_df.isna().mean(axis=0)<nan_threshold]
        self.pivoted_df
        self.pivoted_df=self.pivoted_df.where(pivoted_df <= 100, 100)
        self.pivoted_df  = self.pivoted_df.interpolate()#Llenar los nan que se puedan con interpolacion y los demas con media
        self.pivoted_df  = self.pivoted_df.fillna(pivoted_df.mean())
        self.init_plot(self.ui.tabWidget,graficar_2(self.pivoted_df))

    @color_button('ui','pushButton_escalar')
    def escalar(self):
        if self.ui.comboBox_2.currentText()=='MinMaxScaler':
            scaler = MinMaxScaler(feature_range=(0, 1))
        elif self.ui.comboBox_2.currentText()=='StandardScaler':
            scaler = StandardScaler()
        elif self.ui.comboBox_2.currentText()=='RobustScaler':
            scaler = RobustScaler()
        elif self.ui.comboBox_2.currentText()=='MaxAbsScaler':
            scaler = MaxAbsScaler()
        elif self.ui.comboBox_2.currentText()=='Normalizer':
            scaler = Normalizer()
        elif self.ui.comboBox_2.currentText()=='QuantileTransformer':
            scaler = QuantileTransformer(output_distribution='normal')
        self.df_normalized = pd.DataFrame(scaler.fit_transform(self.pivoted_df))
        self.clear_tabs(self.ui.tabWidget)
        self.init_plot(self.ui.tabWidget,graficar_2(self.df_normalized))
        
    @color_button('ui','pushButton_grafCodo')
    def kmean(self):
        pivoted_df2=self.df_normalized.fillna(0)
        self.X = pivoted_df2.transpose().values
        elbow_data = []

        for n_clusters in range (2,10,1):   
            print(n_clusters) 
            
            km = TimeSeriesKMeans(n_clusters=n_clusters, verbose=False, random_state=42,n_jobs=-1, metric = 'euclidean')
            y_pred = km.fit_predict(self.X)
            
            if n_clusters > 1:
                silueta =  silhouette_score(self.X, km.fit_predict(self.X))
            else:
                silueta = 1
            elbow_data.append((n_clusters, km.inertia_, silueta ))

        df = pd.DataFrame(elbow_data, columns=['clusters', 'distance', 'silhouette'])
        df.set_index(df['clusters'],inplace=True)
        self.clear_tabs(self.ui.tabWidget)
        self.init_plot(self.ui.tabWidget,graficar_2(df[['distance']],df[['silhouette']]))

    @color_button2('ui','pushButton_graficarcluster')
    def graficar_cluster(self,n_clusters=3):
        km = TimeSeriesKMeans(n_clusters, verbose=False, random_state=42,n_jobs=-1, metric = 'euclidean').fit(self.X)
        df_cluster = pd.DataFrame(list(zip(self.pivoted_df.columns, km.labels_)), columns=['metric', 'cluster'])
        centers = km.cluster_centers_
        clasificados_dict = {}
        self.clear_tabs(self.ui.tabWidget)
        for i,j in enumerate(list(set(df_cluster['cluster']))):
            names = list(df_cluster[df_cluster['cluster']==i]['metric'])
            clasificados_dict[i]=self.pivoted_df[names]
            clasificados_dict[i]['PATRON']=centers[i]
            self.init_plot(self.ui.tabWidget,graficar_2(clasificados_dict[j]))

#%% EJECUTAR APP

# from PyQt5 import QtWebEngineWidgets #linea peligrosa

# Configurar la opción de OpenGL antes de crear la instancia de la aplicación
from PyQt5.QtCore import Qt

QtWidgets.QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

app=QtWidgets.QApplication(sys.argv)
myapp=MiFormulario()
myapp.show()
sys.exit(app.exec_())