# FACTUYA – Fundación Ciudad del Saber

Aplicación de escritorio para la gestión y previsualización de facturas en PDF, desarrollada con Python y PySide6.

## Características principales
- Interfaz profesional y moderna
- Branding de Fundación Ciudad del Saber
- Carga de archivos PDF individuales o por carpeta
- Lista de archivos con detalles y tooltips
- Panel de previsualización (placeholder)
- Botones de acción conectados a stubs
- Barra de estado y ProgressBar
- Totalmente en español

## Requisitos
- Python 3.10 o superior
- PySide6 (se instala automáticamente)

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/wandatagles/AplicaciondeFacturas.git
   cd AplicaciondeFacturas
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
Lanza la aplicación con:
```bash
python app.py
```

## Estructura del proyecto
```
.
├─ app.py                  # Punto de entrada
├─ requirements.txt        # Dependencias
├─ README.md               # Este archivo
├─ assets/
│  └─ logo.png             # Logo de la empresa (opcional)
└─ src/
   └─ ui/
      ├─ __init__.py
      ├─ main_window.py    # Ventana principal
      └─ widgets/
         └─ file_list.py   # Widget para lista de archivos
```

## Créditos
Desarrollado por Fundación Ciudad del Saber.

---

¿Dudas o sugerencias? ¡Contáctanos!
