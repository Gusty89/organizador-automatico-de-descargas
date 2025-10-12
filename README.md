# 📁 Organizador-de-archivos

## 🗂️ Estructura del proyecto
Organizador-de-archivos/
│
├── build/ ⚙️ Archivos generados por PyInstaller
├── dist/ ⚙️ Ejecutables finales
├── organizador/
│ ├── src/
│ │ ├── organizador.bat 🖥 Script para Windows
│ │ ├── organizador.py 💻 Código principal
│ │ └── organizador.spec 🛠 Configuración de PyInstaller
├── LICENSE ⚖️ (opcional, ejemplo: MIT License)
├── requirements.txt 📦 Dependencias del proyecto
└── README.md 📘 Documentación y explicación


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

