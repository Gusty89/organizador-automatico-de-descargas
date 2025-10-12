# Estructura del proyecto 📁 Organizador-de-archivos

📁 Organizador-de-archivos
├── 📂 build
├── 📂 dist
├── 📂 organizador
├── 📂 src
│   ├── 📜 organizador.bat
│   ├── 📜 organizador.py 💻 Código principal
│   └── 📜 organizador.spec
├── ⚖️ LICENSE ⚖️ (opcional, por ejemplo MIT License)
├── 📦 requirements.txt 📦 Dependencias (librerías necesarias)
└── 📜 README.md 📘 Explicación del proyecto


# 🧩 Organizador Automático de Descargas

Este proyecto clasifica automáticamente los archivos descargados en carpetas organizadas por tipo (documentos, imágenes, vídeos, etc.), vigilando en tiempo real la carpeta de descargas.

## 🚀 Características
- Monitoreo en tiempo real con `watchdog`
- Interfaz gráfica con `Tkinter`
- Clasificación automática por extensión
- Evita sobrescribir archivos duplicados
- Logs en pantalla

## 🛠️ Instalación
```bash
pip install watchdog (Instala la librería watchdog)
pyinstaller --onefile --windowed organizador.py (Crea el archivo.exe)
pip install -r requirements.txt (Instala las librerías necesarias)
python organizador.py (Ejecuta el archivo en la terminal)
