# 📁 Organizador-de-archivos (Windows)

## 🗂️ Estructura del proyecto

- build/	Carpeta temporal generada por PyInstaller durante la compilación.
- dist/	Contiene los ejecutables finales listos para ser distribuidos.
- organizador/ Archivos de trabajo, temporales e intermedios que PyInstaller generó mientras preparaba el programa para su ejecución como un archivo independiente.
- src/organizador.bat	Script simple para ejecutar el programa en sistemas Windows.
- src/organizador.py	Contiene el código fuente principal del organizador de archivos.
- src/organizador.spec	Archivo de configuración usado por PyInstaller para crear el ejecutable.
- LICENSE	Información sobre la licencia del proyecto (opcional, ej. MIT).
- README.md	Documentación principal del proyecto (este archivo).
- requirements.txt	Lista de dependencias de Python necesarias (bibliotecas).


## 🧩 Descripción del proyecto
**Organizador Automático de Descargas**  
Este proyecto **clasifica automáticamente los archivos descargados** en carpetas organizadas por tipo:

- 📄 Documentos (`.pdf`, `.docx`, `.txt`, etc.)
- 🖼 Imágenes (`.jpg`, `.png`, `.gif`, etc.)
- 🎥 Vídeos (`.mp4`, `.mkv`, `.avi`, etc.)
- 🗃 Otros tipos según extensión

Todo esto ocurre **en tiempo real** mientras descargás archivos en tu carpeta de descargas.

## 🚀 Características
- 👀 **Monitoreo en tiempo real** con `watchdog`
- 🖼 **Interfaz gráfica** con `Tkinter`
- 📂 **Clasificación automática por extensión**
- ❌ **Evita sobrescribir archivos duplicados**
- 📋 **Logs en pantalla** para seguimiento de acciones

## 🛠️ Instalación y uso

### 1️⃣ Instalaciones necesarias
```bash
pip install watchdog (Instala la librería watchdog)
pyinstaller --onefile --windowed organizador.py (Crea el archivo.exe)
pip install -r requirements.txt (Instala las librerías necesarias)
python organizador.py (Ejecuta el archivo en la terminal)

