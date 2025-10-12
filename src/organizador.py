"""
===========================================================
Organizador Automático de Descargas
===========================================================

Autor: Gustavo Paniagua
Versión: 1.0
Lenguaje: Python 3
Dependencias externas:
    - watchdog
    - tkinter (incluido en Python)
    - threading, shutil, os, time

Descripción:
------------
Este programa monitorea en tiempo real la carpeta de descargas del usuario.
Cada vez que se descarga un archivo, el sistema detecta el evento y lo mueve
automáticamente a una carpeta de destino, organizada por tipo de archivo 
(según su extensión).

También permite ejecutar una clasificación inicial de los archivos existentes 
en la carpeta de descargas. Todo el proceso se muestra mediante una interfaz 
gráfica (GUI) en Tkinter.

Estructura general:
-------------------
1. Configuración de rutas y extensiones
2. Funciones de registro (log)
3. Función principal de clasificación de archivos
4. Clasificación de archivos ya existentes
5. Clases de vigilancia basadas en watchdog
6. Interfaz gráfica con botones para iniciar/detener
7. Ejecución principal (mainloop de Tkinter)
"""

import os
import shutil
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ==========================================================
#               CONFIGURACIÓN DE RUTAS
# ==========================================================
DOWNLOADS_FOLDER = r"C:\Users\USUARIO\Downloads"  # Carpeta a vigilar
DEST_FOLDER = r"C:\Users\USUARIO\Desktop\Clasificador"  # Carpeta destino principal
os.makedirs(DEST_FOLDER, exist_ok=True)


# ==========================================================
#           CLASIFICACIÓN SEGÚN TIPO DE ARCHIVO
# ==========================================================
EXT_CARPETAS = {
    "Documentos": ["pdf", "doc", "docx", "txt", "xlsx", "pptx"],
    "Imágenes": ["png", "jpg", "jpeg", "gif", "bmp", "tiff"],
    "Videos": ["mp4", "mkv", "avi", "mov", "wmv"],
    "Comprimidos": ["zip", "rar", "7z", "tar", "gz"],
    "Ejecutables": ["exe", "msi", "bat", "cmd"],
    "Código": ["py", "java", "js", "html", "css", "c", "cpp", "cs", "ts"],
}


# ==========================================================
#                     FUNCIÓN DE LOG
# ==========================================================
def log(mensaje: str):
    """
    Registra un mensaje en el cuadro de texto de la interfaz.
    La función es segura para hilos (usa root.after).

    :param mensaje: Texto que se mostrará en el log.
    """
    def escribir():
        text_log.config(state='normal')
        text_log.insert(tk.END, mensaje + "\n")
        text_log.yview(tk.END)
        text_log.config(state='disabled')
    root.after(0, escribir)


# ==========================================================
#              FUNCIÓN PRINCIPAL DE CLASIFICACIÓN
# ==========================================================
def clasificar_archivo(filepath: str, timeout: int = 10):
    """
    Mueve un archivo desde la carpeta de descargas a su carpeta
    correspondiente dentro del directorio destino, según su extensión.

    :param filepath: Ruta completa del archivo a clasificar.
    :param timeout: Tiempo máximo para intentar acceder al archivo
                    si está bloqueado por el sistema o una aplicación.
    """
    filename = os.path.basename(filepath)
    start_time = time.time()

    # Esperar a que el archivo deje de estar bloqueado
    while True:
        try:
            if os.path.isfile(filepath):
                with open(filepath, 'rb'):
                    break
        except (PermissionError, OSError):
            if time.time() - start_time > timeout:
                log(f"No se pudo mover {filename}: archivo bloqueado")
                return
            time.sleep(0.2)

    # Determinar carpeta de destino según extensión
    ext = os.path.splitext(filename)[1].lower().replace('.', '')
    destino_carpeta = "Otros"

    for carpeta, extensiones in EXT_CARPETAS.items():
        if ext in extensiones:
            destino_carpeta = carpeta
            break

    destino = os.path.join(DEST_FOLDER, destino_carpeta)
    os.makedirs(destino, exist_ok=True)

    # Evitar sobrescribir archivos con el mismo nombre
    destino_final = os.path.join(destino, filename)
    if os.path.exists(destino_final):
        base, extension = os.path.splitext(filename)
        contador = 1
        while os.path.exists(destino_final):
            destino_final = os.path.join(destino, f"{base}({contador}){extension}")
            contador += 1

    # Mover el archivo
    try:
        shutil.move(filepath, destino_final)
        log(f"Movido: {filename} -> {destino_carpeta}")
    except Exception as e:
        log(f"Error moviendo {filename}: {e}")


# ==========================================================
#         CLASIFICACIÓN DE ARCHIVOS YA EXISTENTES
# ==========================================================
def clasificar_existentes():
    """
    Recorre la carpeta de descargas y clasifica todos los archivos
    ya presentes antes de iniciar la vigilancia.
    """
    for filename in os.listdir(DOWNLOADS_FOLDER):
        filepath = os.path.join(DOWNLOADS_FOLDER, filename)
        threading.Thread(target=clasificar_archivo, args=(filepath,), daemon=True).start()


# ==========================================================
#           CLASES DE VIGILANCIA CON WATCHDOG
# ==========================================================
class VigilanciaHandler(FileSystemEventHandler):
    """Maneja los eventos del sistema de archivos (creación de archivos nuevos)."""

    def on_created(self, event):
        """
        Evento que se dispara cuando se crea un nuevo archivo
        en la carpeta vigilada.
        """
        if not event.is_directory:
            threading.Thread(target=clasificar_archivo, args=(event.src_path,), daemon=True).start()


class VigilanciaThread(threading.Thread):
    """
    Hilo de vigilancia que ejecuta el observador de watchdog
    para monitorear la carpeta de descargas en tiempo real.
    """

    def __init__(self):
        super().__init__()
        self.observer = Observer()
        self.stop_event = threading.Event()

    def run(self):
        """Ejecuta el observador hasta que se solicite su detención."""
        event_handler = VigilanciaHandler()
        self.observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)
        self.observer.start()
        log("Vigilancia iniciada...")
        try:
            while not self.stop_event.is_set():
                self.stop_event.wait(1)
        finally:
            self.observer.stop()
            self.observer.join()
            log("Vigilancia detenida")

    def detener(self):
        """Detiene la ejecución del hilo de vigilancia."""
        self.stop_event.set()


# ==========================================================
#               FUNCIONES DE CONTROL DE GUI
# ==========================================================
def iniciar_vigilancia():
    """
    Inicia el proceso de vigilancia de descargas y
    clasifica los archivos existentes.
    """
    global hilo_vigilancia
    threading.Thread(target=clasificar_existentes, daemon=True).start()
    hilo_vigilancia = VigilanciaThread()
    hilo_vigilancia.start()
    lbl_status.config(text="Vigilancia activa...")


def detener_vigilancia():
    """Detiene la vigilancia y muestra un mensaje informativo."""
    if hilo_vigilancia:
        hilo_vigilancia.detener()
        lbl_status.config(text="Vigilancia detenida")
        messagebox.showinfo("Info", "Vigilancia detenida")


# ==========================================================
#                   INTERFAZ GRÁFICA (Tkinter)
# ==========================================================
root = tk.Tk()
root.title("Vigilancia de Descargas Automática")
root.geometry("500x400")

# Etiqueta de estado
lbl_status = tk.Label(root, text="Vigilancia inactiva", font=("Arial", 12))
lbl_status.pack(pady=10)

# Contenedor de botones
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

btn_iniciar = tk.Button(btn_frame, text="Iniciar vigilancia", width=20, command=iniciar_vigilancia)
btn_iniciar.grid(row=0, column=0, padx=5)

btn_detener = tk.Button(btn_frame, text="Detener vigilancia", width=20, command=detener_vigilancia)
btn_detener.grid(row=0, column=1, padx=5)

# Cuadro de texto con scroll para mostrar logs
text_log = scrolledtext.ScrolledText(root, state='disabled', width=60, height=15)
text_log.pack(pady=10)

# Bucle principal de la interfaz
root.mainloop()
