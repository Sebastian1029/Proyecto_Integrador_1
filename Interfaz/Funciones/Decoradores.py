#%% LIBRERIAS
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread


def color_button(sufijo_1, sufijo_2=None):
    def decorator(func):
        def wrapper(self):  # si pongo (self, *args, **kwargs), cuando llame el metodo aunque no tenga argumentos, de por si esta esperandolos, entonces el metodo connect requier si o si llamarlo con "lambda: self.metodo()".
                            #Ademas, al poner self como argumento, quiere decir que es un metodo lo que voy a retorno.
            try:
                resultado = func(self) # si pongo (self, *args, **kwargs), cuando llame el metodo aunque no tenga argumentos, de por si esta esperandolos, entonces el metodo connect requier si o si llamarlo con "lambda: self.metodo()".
                if sufijo_2==None:
                    getattr(self, sufijo_1).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(126, 199, 150, 255));")
                    getattr(self, sufijo_1).setEnabled(True)
                else:
                    getattr(getattr(self, sufijo_1),sufijo_2).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(126, 199, 150, 255));")
                    getattr(getattr(self, sufijo_1),sufijo_2).setEnabled(True)  
                return resultado
            except Exception as e:
                print(f"Error: {e}")
                if sufijo_2==None:
                    getattr(self, sufijo_1).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(199, 0, 0, 255));")
                    getattr(self, sufijo_1).setEnabled(True)
                else:
                    getattr(getattr(self, sufijo_1),sufijo_2).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(199, 0, 0, 255));")
                    getattr(getattr(self, sufijo_1),sufijo_2).setEnabled(True)
        return wrapper
    return decorator

def color_button2(sufijo_1, sufijo_2=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):  # si pongo (self, *args, **kwargs), cuando llame el metodo aunque no tenga argumentos, de por si esta esperandolos, entonces el metodo connect requier si o si llamarlo con "lambda: self.metodo()".
                            #Ademas, al poner self como argumento, quiere decir que es un metodo lo que voy a retorno.
            try:
                resultado = func(self, *args, **kwargs) # si pongo (self, *args, **kwargs), cuando llame el metodo aunque no tenga argumentos, de por si esta esperandolos, entonces el metodo connect requier si o si llamarlo con "lambda: self.metodo()".
                if sufijo_2==None:
                    getattr(self, sufijo_1).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(126, 199, 150, 255));")
                    getattr(self, sufijo_1).setEnabled(True)
                else:
                    getattr(getattr(self, sufijo_1),sufijo_2).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(126, 199, 150, 255));")
                    getattr(getattr(self, sufijo_1),sufijo_2).setEnabled(True)  
                return resultado
            except Exception as e:
                print(f"Error: {e}")
                if sufijo_2==None:
                    getattr(self, sufijo_1).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(199, 0, 0, 255));")
                    getattr(self, sufijo_1).setEnabled(True)
                else:
                    getattr(getattr(self, sufijo_1),sufijo_2).setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.00568182 rgba(230, 230, 230, 255), stop:1 rgba(199, 0, 0, 255));")
                    getattr(getattr(self, sufijo_1),sufijo_2).setEnabled(True)
        return wrapper
    return decorator