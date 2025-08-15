
from PySide6.QtWidgets import (
	QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
	QFileDialog, QListWidget, QSplitter, QStatusBar, QProgressBar, QMessageBox,
	QToolBar, QMenu, QMenuBar
)
from PySide6.QtGui import QKeySequence, QPixmap, QAction, QIcon
from PySide6.QtCore import Qt, QSize
import os
from .theme import theme_manager
from pathlib import Path
from typing import List
try:
	from src.extraction.pipeline import InvoiceExtractionPipeline
	_PIPE_OK = True
except Exception:  # pragma: no cover
	_PIPE_OK = False

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("FACTUYA – Fundación Ciudad del Saber")
		self.setMinimumSize(1080, 680)

		self.pdf_files = []

		central_widget = QWidget()
		main_layout = QVBoxLayout(central_widget)

		# Aplicar tema inicial (claro)
		theme_manager().apply('light')


		# Encabezado con logo y títulos estilizados
		header_layout = QHBoxLayout()
		logo_path = os.path.join(os.path.dirname(__file__), '../../assets/logo.png')
		logo_label = QLabel()
		logo_label.setObjectName("logoLabel")
		if os.path.exists(logo_path):
			pixmap = QPixmap(logo_path)
			logo_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		else:
			logo_label.setText("[Logo]")
			logo_label.setFixedSize(64, 64)
			logo_label.setAlignment(Qt.AlignCenter)
		header_layout.addWidget(logo_label)

		# Título principal y subtítulo con estilos
		title_widget = QWidget()
		title_layout = QVBoxLayout(title_widget)
		title_layout.setContentsMargins(0, 0, 0, 0)

		app_label = QLabel('<span style="font-family:Segoe UI,Arial,sans-serif;font-size:2.6em;font-weight:800;color:#2980b9;letter-spacing:2px;">FACTUYA</span>')
		app_label.setObjectName("appLabel")
		app_label.setAlignment(Qt.AlignLeft)
		title_layout.addWidget(app_label)

		empresa_label = QLabel('<span style="font-family:Segoe UI,Arial,sans-serif;font-size:1.2em;font-weight:500;color:#16a085;letter-spacing:1px;">Fundación Ciudad del Saber</span>')
		empresa_label.setObjectName("empresaLabel")
		empresa_label.setAlignment(Qt.AlignLeft)
		title_layout.addWidget(empresa_label)

		header_layout.addWidget(title_widget)
		header_layout.addStretch()
		main_layout.addLayout(header_layout)

		# Toolbar moderna
		toolbar = QToolBar("Acciones")
		toolbar.setIconSize(QSize(20,20))
		self.addToolBar(Qt.TopToolBarArea, toolbar)

		a_cargar = QAction(QIcon.fromTheme("document-open"), "Cargar PDF…", self)
		a_cargar.setShortcut(QKeySequence("Ctrl+O"))
		a_cargar.setToolTip("Selecciona un archivo PDF")
		a_cargar.triggered.connect(self.on_cargar_pdf)
		toolbar.addAction(a_cargar)

		a_carpeta = QAction(QIcon.fromTheme("folder-open"), "Importar carpeta…", self)
		a_carpeta.setShortcut(QKeySequence("Ctrl+Shift+O"))
		a_carpeta.setToolTip("Importa todos los PDFs de una carpeta")
		a_carpeta.triggered.connect(self.on_importar_carpeta)
		toolbar.addAction(a_carpeta)

		toolbar.addSeparator()

		a_extraer = QAction(QIcon.fromTheme("edit-copy"), "Extraer tablas", self)
		a_extraer.setShortcut(QKeySequence("Ctrl+T"))
		a_extraer.triggered.connect(self.on_extraer_tablas)
		toolbar.addAction(a_extraer)

		a_exportar = QAction(QIcon.fromTheme("document-save"), "Exportar a Excel", self)
		a_exportar.setShortcut(QKeySequence("Ctrl+E"))
		a_exportar.triggered.connect(self.on_exportar_excel)
		toolbar.addAction(a_exportar)

		a_limpiar = QAction(QIcon.fromTheme("edit-delete"), "Limpiar información", self)
		a_limpiar.setShortcut(QKeySequence("Ctrl+L"))
		a_limpiar.triggered.connect(self.on_limpiar_informacion)
		toolbar.addAction(a_limpiar)

		toolbar.addSeparator()
		a_tema = QAction(QIcon.fromTheme("preferences-desktop-theme"), "Alternar tema", self)
		a_tema.setShortcut(QKeySequence("Ctrl+Shift+T"))
		a_tema.triggered.connect(lambda: theme_manager().toggle())
		toolbar.addAction(a_tema)

		self.label_archivos = QLabel("0 archivos cargados")
		self.label_archivos.setObjectName("labelArchivos")
		toolbar.addSeparator()
		toolbar.addWidget(self.label_archivos)

		# Splitter central: lista de archivos y previsualización
		splitter = QSplitter(Qt.Horizontal)
		self.list_widget = QListWidget()
		self.list_widget.setToolTip("Lista de archivos PDF cargados")
		self.list_widget.itemSelectionChanged.connect(self.on_seleccion_archivo)
		splitter.addWidget(self.list_widget)

		self.preview_widget = QLabel("Previsualización no implementada")
		self.preview_widget.setObjectName("previewLabel")
		self.preview_widget.setAlignment(Qt.AlignCenter)
		splitter.addWidget(self.preview_widget)
		splitter.setSizes([300, 600])
		main_layout.addWidget(splitter)

		# (Acciones movidas a la toolbar para diseño moderno)

		# Barra de estado y ProgressBar
		self.status_bar = QStatusBar()
		self.setStatusBar(self.status_bar)
		self.status_bar.showMessage("Listo")

		self.progress_bar = QProgressBar()
		self.progress_bar.setVisible(False)
		self.status_bar.addPermanentWidget(self.progress_bar)

		self.setCentralWidget(central_widget)

	# Métodos stub para acciones
	def on_cargar_pdf(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona un PDF", "", "PDF Files (*.pdf)")
		if file_path:
			self.agregar_pdf(file_path)

	def on_importar_carpeta(self):
		folder = QFileDialog.getExistingDirectory(self, "Selecciona una carpeta")
		if folder:
			count = 0
			for fname in os.listdir(folder):
				if fname.lower().endswith('.pdf'):
					fpath = os.path.join(folder, fname)
					if self.agregar_pdf(fpath):
						count += 1
			QMessageBox.information(self, "Importación", f"Se importaron {count} archivos PDF.")

	def agregar_pdf(self, file_path):
		if not file_path.lower().endswith('.pdf'):
			QMessageBox.warning(self, "Error", "El archivo seleccionado no es un PDF.")
			return False
		if file_path in self.pdf_files:
			QMessageBox.information(self, "Duplicado", "Este archivo ya fue cargado.")
			return False
		self.pdf_files.append(file_path)
		self.list_widget.addItem(os.path.basename(file_path))
		item = self.list_widget.item(self.list_widget.count()-1)
		item.setToolTip(file_path)
		self.label_archivos.setText(f"{len(self.pdf_files)} archivos cargados")
		self.status_bar.showMessage(f"{len(self.pdf_files)} PDF cargados")
		return True

	def on_seleccion_archivo(self):
		selected_items = self.list_widget.selectedItems()
		if selected_items:
			idx = self.list_widget.row(selected_items[0])
			file_name = os.path.basename(self.pdf_files[idx])
			self.preview_widget.setText(f"{file_name}\nPrevisualización no implementada")
		else:
			self.preview_widget.setText("Previsualización no implementada")

	def on_extraer_tablas(self):
		if not self.pdf_files:
			QMessageBox.information(self, "Extracción", "No hay PDFs cargados.")
			return
		if not _PIPE_OK:
			QMessageBox.warning(self, "Extracción", "Pipeline no disponible (dependencias faltantes).")
			return
		from src.extraction.pipeline import InvoiceExtractionPipeline
		pipeline = InvoiceExtractionPipeline()
		paths = [Path(p) for p in self.pdf_files]
		result = pipeline.extract_batch(paths)
		rows = len(result.rows)
		msg = f"Extracción simulada completada. Filas: {rows}"
		if result.warnings:
			msg += "\nWarnings:\n- " + "\n- ".join(result.warnings)
		QMessageBox.information(self, "Extracción", msg)

	def on_exportar_excel(self):
		QMessageBox.information(self, "Exportar a Excel", "Función no implementada.")

	def on_limpiar_informacion(self):
		self.pdf_files.clear()
		self.list_widget.clear()
		self.label_archivos.setText("0 archivos cargados")
		self.preview_widget.setText("Previsualización no implementada")
		self.status_bar.showMessage("Listo")
