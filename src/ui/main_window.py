
from PySide6.QtWidgets import (
	QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
	QFileDialog, QListWidget, QSplitter, QStatusBar, QProgressBar, QToolBar, QMessageBox
)
from PySide6.QtGui import QIcon, QKeySequence, QPixmap, QAction
from PySide6.QtCore import Qt, QSize
import os


# Ventana principal de la aplicación
from PySide6.QtWidgets import (
	QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
	QFileDialog, QListWidget, QSplitter, QStatusBar, QProgressBar, QMessageBox
)
from PySide6.QtGui import QKeySequence, QPixmap
from PySide6.QtCore import Qt
import os

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Facturas – Fundación Ciudad del Saber")
		self.setMinimumSize(900, 600)

		self.pdf_files = []

		central_widget = QWidget()
		main_layout = QVBoxLayout(central_widget)

		self.setStyleSheet("""
			QMainWindow {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
					stop:0 #f5f7fa, stop:1 #c3cfe2);
			}
			QLabel#titleLabel {
				font-size: 2em;
				font-weight: bold;
				color: #2c3e50;
				margin-left: 12px;
			}
			QLabel#logoLabel {
				border-radius: 8px;
				background: #e0e7ef;
				border: 1px solid #b0b8c1;
			}
			QPushButton {
				background-color: #2980b9;
				color: white;
				border-radius: 6px;
				padding: 8px 18px;
				font-size: 1em;
				font-weight: 500;
				margin-right: 8px;
			}
			QPushButton:hover {
				background-color: #3498db;
			}
			QPushButton:pressed {
				background-color: #1c5a85;
			}
			QListWidget {
				background: #f8fafc;
				border: 1px solid #b0b8c1;
				border-radius: 6px;
				font-size: 1em;
			}
			QStatusBar {
				background: #e0e7ef;
				color: #2c3e50;
				font-weight: 500;
				border-top: 1px solid #b0b8c1;
			}
			QProgressBar {
				border-radius: 6px;
				background: #f5f7fa;
				height: 18px;
			}
			QProgressBar::chunk {
				background-color: #2980b9;
				border-radius: 6px;
			}
			QLabel#previewLabel {
				background: #f8fafc;
				border: 1px dashed #b0b8c1;
				border-radius: 8px;
				color: #7f8c8d;
				font-size: 1.1em;
				padding: 24px;
			}
		""")


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

		# Zona superior: botones y label de archivos
		top_layout = QHBoxLayout()
		self.btn_cargar_pdf = QPushButton("Cargar PDF…")
		self.btn_cargar_pdf.setToolTip("Selecciona un archivo PDF")
		self.btn_cargar_pdf.setShortcut(QKeySequence("Ctrl+O"))
		self.btn_cargar_pdf.clicked.connect(self.on_cargar_pdf)
		top_layout.addWidget(self.btn_cargar_pdf)

		self.btn_importar_carpeta = QPushButton("Importar carpeta…")
		self.btn_importar_carpeta.setToolTip("Importa todos los PDFs de una carpeta")
		self.btn_importar_carpeta.setShortcut(QKeySequence("Ctrl+Shift+O"))
		self.btn_importar_carpeta.clicked.connect(self.on_importar_carpeta)
		top_layout.addWidget(self.btn_importar_carpeta)

		self.label_archivos = QLabel("0 archivos cargados")
		top_layout.addWidget(self.label_archivos)
		top_layout.addStretch()
		main_layout.addLayout(top_layout)

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

		# Barra de acciones (debajo del splitter)
		actions_layout = QHBoxLayout()
		self.btn_extraer_tablas = QPushButton("Extraer tablas")
		self.btn_extraer_tablas.setToolTip("Extrae las tablas de los PDFs")
		self.btn_extraer_tablas.setShortcut(QKeySequence("Ctrl+T"))
		self.btn_extraer_tablas.clicked.connect(self.on_extraer_tablas)
		actions_layout.addWidget(self.btn_extraer_tablas)

		self.btn_exportar_excel = QPushButton("Exportar a Excel")
		self.btn_exportar_excel.setToolTip("Exporta los datos a un archivo Excel")
		self.btn_exportar_excel.setShortcut(QKeySequence("Ctrl+E"))
		self.btn_exportar_excel.clicked.connect(self.on_exportar_excel)
		actions_layout.addWidget(self.btn_exportar_excel)

		self.btn_limpiar_info = QPushButton("Limpiar información")
		self.btn_limpiar_info.setToolTip("Limpia la lista y la previsualización")
		self.btn_limpiar_info.setShortcut(QKeySequence("Ctrl+L"))
		self.btn_limpiar_info.clicked.connect(self.on_limpiar_informacion)
		actions_layout.addWidget(self.btn_limpiar_info)

		actions_layout.addStretch()
		main_layout.addLayout(actions_layout)

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
		QMessageBox.information(self, "Extraer tablas", "Función no implementada.")

	def on_exportar_excel(self):
		QMessageBox.information(self, "Exportar a Excel", "Función no implementada.")

	def on_limpiar_informacion(self):
		self.pdf_files.clear()
		self.list_widget.clear()
		self.label_archivos.setText("0 archivos cargados")
		self.preview_widget.setText("Previsualización no implementada")
		self.status_bar.showMessage("Listo")
