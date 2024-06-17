
#%%
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFrame
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import pyqtSlot, QObject, QEvent
import plotly.io as pio
import json

class PlotlyBridge(QObject):
    def __init__(self, plotly_widget, x_range,y_range,parent=None):
        super().__init__(parent)
        self.plotly_widget = plotly_widget
        self.parent = parent  # Guardar la referencia al padre
        self.x_range = x_range
        self.y_range = y_range

    @pyqtSlot(str)
    def onZoom(self, eventdata):
        eventdata = json.loads(eventdata)
        self.x_range = eventdata.get("xaxis.range[0]", None), eventdata.get("xaxis.range[1]", None)
        self.y_range = eventdata.get("yaxis.range[0]", None), eventdata.get("yaxis.range[1]", None)
        
        
        # Si los rangos no están presentes, tratamos de obtener los valores actuales de los ejes
        if self.x_range == (None, None) or self.y_range == (None, None):
            print('prueba si estoy entrando aqui')
            self.plotly_widget.request_axes_ranges()


        self.get_zoom_range()
        if self.parent:
            self.parent.ui_calidad.actualizarfecha()  # Asegurarse de que el padre tenga el método actualizarfecha

    def get_zoom_range(self):
        return self.x_range, self.y_range

class PlotlyWidget(QWidget):
    def __init__(self, x_range,y_range,parent=None):
        super().__init__(parent)
        self.parent = parent  # Guardar la referencia al padre
        self.x_range=x_range
        self.y_range=y_range
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.plot_div = QWebEngineView(self)
        layout.addWidget(self.plot_div)
        self.setLayout(layout)

        # Configurar QWebChannel
        self.bridge = PlotlyBridge(self,self.x_range,self.y_range,self.parent)
        self.channel = QWebChannel()
        self.channel.registerObject("plotlyBridge", self.bridge)
        self.plot_div.page().setWebChannel(self.channel)

        # Asegurarse de que el gráfico se redimensione con la ventana
        self.installEventFilter(self)
        self.plot_div.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize and source == self:
            self.resize_plot()
        elif event.type() == QEvent.FocusIn and source == self.plot_div:
            self.auto_scale_plot()
        return super().eventFilter(source, event)

    def resize_plot(self):
        self.plot_div.page().runJavaScript('Plotly.Plots.resize(document.getElementById("plotly-div"));')

    def auto_scale_plot(self):
        self.plot_div.page().runJavaScript('Plotly.relayout(document.getElementById("plotly-div"), {{xaxis: {{autorange: true}}, yaxis: {{autorange: true}}}});')

    def update_plot(self, figure):
        figure.update_layout(autosize=True)
        figure_json = pio.to_json(figure)

        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    new QWebChannel(qt.webChannelTransport, function(channel) {{
                        window.plotlyBridge = channel.objects.plotlyBridge;
                        var figure = {figure_json};
                        Plotly.newPlot('plotly-div', figure.data, figure.layout).then(function() {{
                            var plotlyDiv = document.getElementById('plotly-div');
                            plotlyDiv.on('plotly_relayout', function (eventdata) {{
                                window.plotlyBridge.onZoom(JSON.stringify(eventdata));
                            }});
                        }});
                    }});
                }});
                function getCurrentRanges() {{
                    var plotlyDiv = document.getElementById('plotly-div');
                    var xRange = plotlyDiv.layout.xaxis.range;
                    var yRange = plotlyDiv.layout.yaxis.range;
                    return {{
                        xRange: xRange,
                        yRange: yRange
                    }};
                }}
                function requestAxesRanges() {{
                    var ranges = getCurrentRanges();
                    window.plotlyBridge.onZoom(JSON.stringify({{
                        "xaxis.range[0]": ranges.xRange[0],
                        "xaxis.range[1]": ranges.xRange[1],
                        "yaxis.range[0]": ranges.yRange[0],
                        "yaxis.range[1]": ranges.yRange[1]
                    }}));
                }}    
            </script>
            <style>
                html, body {{
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
                #plotly-div {{
                    width: 100%;
                    height: 100%;
                }}
            </style>
        </head>
        <body>
            <div id="plotly-div"></div>
        </body>
        </html>
        '''

        self.plot_div.setHtml(html)

    def request_axes_ranges(self):
        print(self.plot_div.page().runJavaScript('requestAxesRanges();'))

class Multigrafica(QObject):

    def __init__(self, parent=None):
        self.parent = parent  # Guardar la referencia al padre
        self.Plot_widgets = {}

    def agg_grafica(self, frame, fig):
        layout = frame.layout()
        self.x_range=fig.layout.xaxis.range if fig.layout.xaxis.range else [None, None]
        print('voyy dad ')
        print(self.x_range)
        self.y_range= fig.layout.yaxis.range if fig.layout.yaxis.range else [None, None]
        if layout is None:
            layout = QtWidgets.QVBoxLayout(frame)
            frame.setLayout(layout)

        # Limpiar el contenido anterior del layout
        self.clear_layout(layout)

        self.plot_widget = PlotlyWidget(self.x_range,self.y_range,self.parent)

        # Agregar el QWebEngineView al layout de frame
        layout.addWidget(self.plot_widget)
        self.plot_widget.update_plot(fig)

    def print_zoom_range(self):
        # Acceder al rango de zoom y imprimirlo
        self.bridge = self.plot_widget.bridge
        x_range, y_range = self.bridge.get_zoom_range()
        print("X Range:", x_range)
        print("Y Range:", y_range)

    def clear_layout(self, layout):
        # Eliminar todos los widgets dentro del layout
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def clear_tabs(self, tab_widget):
        while tab_widget.count() > 0:
            tab_widget.removeTab(0)

    def add_tabs(self, tab_widget, tabs_list):
        for tab_name in tabs_list:
            new_tab = QWidget()
            layout = QVBoxLayout()
            frame = QFrame(new_tab)
            frame.setFrameShape(QFrame.StyledPanel)
            layout.addWidget(frame)
            new_tab.setLayout(layout)
            tab_widget.addTab(new_tab, tab_name)

    def update_tabs(self, tab_widget, tabs_list):
        self.clear_tabs(tab_widget)
        self.add_tabs(tab_widget, tabs_list)

    def agregar_grafica_tab(self, tab_widget, tab_index, fig):
        current_tab_widget = tab_widget.widget(tab_index)
        layout = current_tab_widget.layout()

        if isinstance(layout, QVBoxLayout):
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item.widget(), QFrame):
                    frame = item.widget()
                    if frame.layout() is None:
                        frame.setLayout(QVBoxLayout()) 

                    # Llamar a la función agg_grafica para agregar el gráfico
                    self.agg_grafica(frame, fig)

                    # Almacenar plotlywidget en el diccionario
                    self.Plot_widgets[tab_index] = self.plot_widget

            print("No se encontró un marco dentro del QVBoxLayout.")
        else:
            print("La pestaña actual no tiene un QVBoxLayout.")
