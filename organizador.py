import os
import shutil
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ===================== Rutas absolutas =====================
DOWNLOADS_FOLDER = r"C:\Users\USUARIO\Downloads"  # Carpeta a vigilar
DEST_FOLDER = r"C:\Users\USUARIO\Desktop\Clasificador"  # Carpeta destino principal
os.makedirs(DEST_FOLDER, exist_ok=True)

# ===================== Diccionario de extensiones =====================
EXT_CARPETAS = {
    "Documentos": ["pdf", "doc", "docx", "txt", "xlsx", "pptx"],
    "Imágenes": ["png", "jpg", "jpeg", "gif", "bmp", "tiff"],
    "Videos": ["mp4", "mkv", "avi", "mov", "wmv"],
    "Comprimidos": ["zip", "rar", "7z", "tar", "gz"],
    "Ejecutables": ["exe", "msi", "bat", "cmd"],
    "Código": ["py", "java", "js", "html", "css", "c", "cpp", "cs", "ts"],
}

# ===================== Función para log =====================
def log(mensaje):
    def escribir():
        text_log.config(state='normal')
        text_log.insert(tk.END, mensaje + "\n")
        text_log.yview(tk.END)
        text_log.config(state='disabled')
    root.after(0, escribir)

# ===================== Función para mover archivos =====================
def clasificar_archivo(filepath, timeout=10):
    filename = os.path.basename(filepath)
    start_time = time.time()

    # Esperar a que el archivo esté listo (no bloqueado)
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

    # Obtener extensión y determinar carpeta destino
    ext = os.path.splitext(filename)[1].lower().replace('.', '')
    destino_carpeta = "Otros"

    for carpeta, extensiones in EXT_CARPETAS.items():
        if ext in extensiones:
            destino_carpeta = carpeta
            break

    destino = os.path.join(DEST_FOLDER, destino_carpeta)
    os.makedirs(destino, exist_ok=True)

    # Evitar sobrescribir archivos
    destino_final = os.path.join(destino, filename)
    if os.path.exists(destino_final):
        base, extension = os.path.splitext(filename)
        contador = 1
        while os.path.exists(destino_final):
            destino_final = os.path.join(destino, f"{base}({contador}){extension}")
            contador += 1

    try:
        shutil.move(filepath, destino_final)
        log(f"Movido: {filename} -> {destino_carpeta}")
    except Exception as e:
        log(f"Error moviendo {filename}: {e}")

# ===================== Clasificar archivos existentes =====================
def clasificar_existentes():
    for filename in os.listdir(DOWNLOADS_FOLDER):
        filepath = os.path.join(DOWNLOADS_FOLDER, filename)
        threading.Thread(target=clasificar_archivo, args=(filepath,), daemon=True).start()

# ===================== Clase de vigilancia =====================
class VigilanciaHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            threading.Thread(target=clasificar_archivo, args=(event.src_path,), daemon=True).start()

class VigilanciaThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.observer = Observer()
        self.stop_event = threading.Event()

    def run(self):
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
        self.stop_event.set()

# ===================== Funciones de la GUI =====================
def iniciar_vigilancia():
    global hilo_vigilancia
    threading.Thread(target=clasificar_existentes, daemon=True).start()
    hilo_vigilancia = VigilanciaThread()
    hilo_vigilancia.start()
    lbl_status.config(text="Vigilancia activa...")

def detener_vigilancia():
    if hilo_vigilancia:
        hilo_vigilancia.detener()
        lbl_status.config(text="Vigilancia detenida")
        messagebox.showinfo("Info", "Vigilancia detenida")

# ===================== Crear GUI =====================
root = tk.Tk()
root.title("Vigilancia de Descargas")
root.geometry("500x400")

lbl_status = tk.Label(root, text="Vigilancia inactiva", font=("Arial", 12))
lbl_status.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

btn_iniciar = tk.Button(btn_frame, text="Iniciar vigilancia", width=20, command=iniciar_vigilancia)
btn_iniciar.grid(row=0, column=0, padx=5)

btn_detener = tk.Button(btn_frame, text="Detener vigilancia", width=20, command=detener_vigilancia)
btn_detener.grid(row=0, column=1, padx=5)

text_log = scrolledtext.ScrolledText(root, state='disabled', width=60, height=15)
text_log.pack(pady=10)

root.mainloop()
