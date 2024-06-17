# Proyecto_Integrador_1

https://github.com/Sebastian1029/Proyecto_Integrador_1

En este repositorio está contenido el proyecto integrador por 

Los códigos contenidos están diseñados para ejecutarse en un entorno de aws conectandose con un bucket de s3.

# Codigos aws

1. Ingesta.ipynb

Este notebook hace la transferencia de datos desde el servidor sftp de tigo hacia el bucket de s3, en este se selecciona el mes del cual se desean obtener los datos

2. Trusted.ipynb

Este notebook realiza el proceso de estructuración del archivo trusted que será la fuente del modelo, recolecta la información de la carpeta raw del datalake y la almacena en la carpeta trusted

3. IngestaDiaria.ipynb

Este notebook realiza el proceso de ingesta de los datos más recientes del sftp, también hace la conversión a trusted y la concatena con el archivo trsuted.csv del mes actual

4. Proyecto.ipynb

Este notebook ejecuta la transformación del archivo trusted, se preprocesmiento y su analisis, también ejecuta el modelo de series de tiempo

5. Predicción.ipynb

Este notebook permite cargar un modelo ya entrenado y hace clasificaciones sobre el archivo trusted.


# Interfaz
En la carpeta interfaz se encuentra el odigo y las dependencias para ejecutar el aplicativo.




