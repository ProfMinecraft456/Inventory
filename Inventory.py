import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QWidget, QMessageBox, QHeaderView,
                            QGroupBox, QFormLayout, QCompleter, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont


class InventarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inventario y Ventas")
        self.setGeometry(100, 100, 1000, 850)
        
        # Configurar paleta de colores
        self.setup_estilos()
        
        # Cargar datos existentes o crear uno nuevo
        self.archivo_json = "Inventory.json"
        self.datos = self.cargar_datos()
        
        # Variables para ventas
        self.venta_actual = []
        self.total_venta = 0
        
        # Widget central y QTabWidget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)
        
        self.tab_widget = QTabWidget()
        self.layout_principal.addWidget(self.tab_widget)
        
        # Pestaña Inventario
        self.tab_inventario = QWidget()
        self.tab_inventario_layout = QVBoxLayout()
        self.tab_inventario.setLayout(self.tab_inventario_layout)
        
        # Secciones para Inventario
        self.crear_seccion_busqueda(self.tab_inventario_layout)
        self.crear_seccion_agregar(self.tab_inventario_layout)
        self.crear_tabla_inventario(self.tab_inventario_layout)
        self.crear_botones_inventario(self.tab_inventario_layout)  # Botones solo para Inventario
        
        # Pestaña Ventas
        self.tab_ventas = QWidget()
        self.tab_ventas_layout = QVBoxLayout()
        self.tab_ventas.setLayout(self.tab_ventas_layout)
        
        # Secciones para Ventas
        self.crear_seccion_ventas(self.tab_ventas_layout)
        self.crear_tabla_venta(self.tab_ventas_layout)
        self.crear_seccion_pago(self.tab_ventas_layout)
        self.crear_botones_ventas(self.tab_ventas_layout)  # Botón Finalizar Venta aquí
        
        self.tab_widget.addTab(self.tab_inventario, "Inventario")
        self.tab_widget.addTab(self.tab_ventas, "Ventas")
        
        # Actualizar tabla y autocompletado
        self.actualizar_tabla()
        self.actualizar_completer()

    # ======================= MÉTODOS PRINCIPALES =======================
    def setup_estilos(self):
        """Configura los estilos de la aplicación."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#F6F0F0'))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor('#F2E2B1'))
        palette.setColor(QPalette.AlternateBase, QColor('#D5C7A3'))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor('#BDB395'))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor('#D5C7A3'))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #333333;
            }
            
            QLineEdit, QTableWidget {
                border: 1px solid #BDB395;
                border-radius: 4px;
                padding: 3px;
            }
            
            QPushButton {
                border: 1px solid #8A7F68;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background: #D5C7A3;
            }
            
            QHeaderView::section {
                background-color: #BDB395;
                padding: 4px;
                border: 1px solid #8A7F68;
                font-weight: bold;
            }
            
            QTableWidget {
                gridline-color: #BDB395;
                selection-background-color: #D5C7A3;
                selection-color: black;
            }
            
            QGroupBox {
                border: 1px solid #BDB395;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            
            QTabBar::tab {
                background: #F2E2B1;
                color: #333333;
                border: 1px solid #BDB395;
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background: #D5C7A3;
                border-bottom: 2px solid #F6F0F0;
            }
            
            QLineEdit[error="true"] {
                border: 1px solid red;
                color: red;
            }
        """)

    def cargar_datos(self):
        """Carga los datos desde el archivo JSON o crea uno nuevo si no existe."""
        if os.path.exists(self.archivo_json):
            with open(self.archivo_json, 'r') as f:
                try:
                    data = json.load(f)
                    if "Products" not in data:
                        data = {"Products": data}
                    return data["Products"]
                except json.JSONDecodeError:
                    return {}
        else:
            with open(self.archivo_json, 'w') as f:
                json.dump({"Products": {}}, f)
            return {}

    def guardar_datos(self):
        """Guarda los datos en el archivo JSON."""
        with open(self.archivo_json, 'w') as f:
            json.dump({"Products": self.datos}, f, indent=4)

    # ======================= SECCIÓN INVENTARIO =======================
    def crear_seccion_busqueda(self, parent_layout):
        """Crea la sección de búsqueda de artículos."""
        layout_busqueda = QHBoxLayout()
        layout_busqueda.setContentsMargins(5, 5, 5, 5)
        
        self.label_buscar = QLabel("Buscar Artículo:")
        self.label_buscar.setFont(QFont('Arial', 10))
        
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Escriba para buscar...")
        self.input_buscar.setFont(QFont('Arial', 10))
        self.input_buscar.textChanged.connect(self.buscar_en_tiempo_real)
        
        layout_busqueda.addWidget(self.label_buscar)
        layout_busqueda.addWidget(self.input_buscar)
        
        parent_layout.addLayout(layout_busqueda)

    def crear_seccion_agregar(self, parent_layout):
        """Crea la sección para agregar/actualizar artículos."""
        layout_agregar = QHBoxLayout()
        layout_agregar.setContentsMargins(5, 5, 5, 5)
        
        self.label_nombre = QLabel("Nombre:")
        self.label_nombre.setFont(QFont('Arial', 10))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del artículo")
        self.input_nombre.setFont(QFont('Arial', 10))
        
        self.label_precio = QLabel("Precio Unitario:")
        self.label_precio.setFont(QFont('Arial', 10))
        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Ej: 4000 COP")
        self.input_precio.setFont(QFont('Arial', 10))
        
        self.label_stock = QLabel("Stock Actual:")
        self.label_stock.setFont(QFont('Arial', 10))
        self.input_stock = QLineEdit()
        self.input_stock.setPlaceholderText("Cantidad disponible")
        self.input_stock.setFont(QFont('Arial', 10))
        
        self.boton_agregar = QPushButton("Agregar/Actualizar")
        self.boton_agregar.setFont(QFont('Arial', 10, QFont.Bold))
        self.boton_agregar.clicked.connect(self.agregar_actualizar_articulo)
        
        layout_agregar.addWidget(self.label_nombre)
        layout_agregar.addWidget(self.input_nombre)
        layout_agregar.addWidget(self.label_precio)
        layout_agregar.addWidget(self.input_precio)
        layout_agregar.addWidget(self.label_stock)
        layout_agregar.addWidget(self.input_stock)
        layout_agregar.addWidget(self.boton_agregar)
        
        parent_layout.addLayout(layout_agregar)

    def crear_tabla_inventario(self, parent_layout):
        """Crea la tabla que muestra el inventario."""
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Artículo", "Precio Unitario", "Stock Actual"])
        self.tabla.setSortingEnabled(True)
        
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.itemSelectionChanged.connect(self.cargar_datos_seleccionados)
        
        self.tabla.setFont(QFont('Arial', 10))
        self.tabla.setAlternatingRowColors(True)
        
        parent_layout.addWidget(self.tabla)

    def crear_botones_inventario(self, parent_layout):
        """Crea botones para la pestaña de Inventario."""
        layout_botones = QHBoxLayout()
        layout_botones.setContentsMargins(5, 5, 5, 5)
        
        self.boton_eliminar = QPushButton("Eliminar Artículo")
        self.boton_eliminar.setFont(QFont('Arial', 10))
        self.boton_eliminar.clicked.connect(self.eliminar_articulo)
        
        self.boton_limpiar = QPushButton("Limpiar Campos")
        self.boton_limpiar.setFont(QFont('Arial', 10))
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        
        self.boton_mostrar_todo = QPushButton("Mostrar Todo")
        self.boton_mostrar_todo.setFont(QFont('Arial', 10))
        self.boton_mostrar_todo.clicked.connect(self.mostrar_todo)
        
        layout_botones.addWidget(self.boton_eliminar)
        layout_botones.addWidget(self.boton_limpiar)
        layout_botones.addWidget(self.boton_mostrar_todo)
        
        parent_layout.addLayout(layout_botones)

    # ======================= SECCIÓN VENTAS =======================
    def crear_seccion_ventas(self, parent_layout):
        """Crea la sección para realizar ventas."""
        groupbox = QGroupBox("Módulo de Ventas")
        layout_ventas = QFormLayout()
        
        self.label_producto_venta = QLabel("Producto:")
        self.input_producto_venta = QLineEdit()
        self.input_producto_venta.setPlaceholderText("Nombre del producto")
        self.input_producto_venta.textChanged.connect(self.actualizar_precio_venta)
        
        self.label_precio_venta = QLabel("Precio Unitario:")
        self.input_precio_venta = QLineEdit()
        self.input_precio_venta.setReadOnly(True)
        
        self.label_cantidad_venta = QLabel("Cantidad:")
        self.input_cantidad_venta = QLineEdit()
        self.input_cantidad_venta.setPlaceholderText("Cantidad a vender")
        self.input_cantidad_venta.textChanged.connect(self.validar_stock_venta)
        
        self.label_total_producto = QLabel("Total Producto:")
        self.input_total_producto = QLineEdit()
        self.input_total_producto.setReadOnly(True)
        
        self.boton_agregar_venta = QPushButton("Agregar a Venta")
        self.boton_agregar_venta.clicked.connect(self.agregar_a_venta)
        
        layout_ventas.addRow(self.label_producto_venta, self.input_producto_venta)
        layout_ventas.addRow(self.label_precio_venta, self.input_precio_venta)
        layout_ventas.addRow(self.label_cantidad_venta, self.input_cantidad_venta)
        layout_ventas.addRow(self.label_total_producto, self.input_total_producto)
        layout_ventas.addRow(self.boton_agregar_venta)
        
        groupbox.setLayout(layout_ventas)
        parent_layout.addWidget(groupbox)

    def crear_tabla_venta(self, parent_layout):
        """Crea la tabla que muestra los productos en la venta actual."""
        self.tabla_venta = QTableWidget()
        self.tabla_venta.setColumnCount(4)
        self.tabla_venta.setHorizontalHeaderLabels(["Producto", "Precio Unitario", "Cantidad", "Total"])
        self.tabla_venta.setSortingEnabled(False)
        
        header = self.tabla_venta.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        self.tabla_venta.setFont(QFont('Arial', 10))
        self.tabla_venta.setAlternatingRowColors(True)
        
        parent_layout.addWidget(self.tabla_venta)

    def crear_seccion_pago(self, parent_layout):
        """Crea la sección para el pago y cálculo de cambio."""
        groupbox = QGroupBox("Pago y Cambio")
        layout_pago = QFormLayout()
        
        self.label_total_venta = QLabel("Total Venta:")
        self.input_total_venta = QLineEdit()
        self.input_total_venta.setReadOnly(True)
        self.input_total_venta.setFont(QFont('Arial', 10, QFont.Bold))
        
        self.label_dinero_recibido = QLabel("Dinero Recibido:")
        self.input_dinero_recibido = QLineEdit()
        self.input_dinero_recibido.setPlaceholderText("Ingrese el monto recibido")
        self.input_dinero_recibido.textChanged.connect(self.calcular_cambio)
        
        self.label_cambio = QLabel("Cambio:")
        self.input_cambio = QLineEdit()
        self.input_cambio.setReadOnly(True)
        self.input_cambio.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_cambio.setStyleSheet("color: green;")
        
        layout_pago.addRow(self.label_total_venta, self.input_total_venta)
        layout_pago.addRow(self.label_dinero_recibido, self.input_dinero_recibido)
        layout_pago.addRow(self.label_cambio, self.input_cambio)
        
        groupbox.setLayout(layout_pago)
        parent_layout.addWidget(groupbox)

    def crear_botones_ventas(self, parent_layout):
        """Crea botones para la pestaña de Ventas."""
        layout_botones = QHBoxLayout()
        layout_botones.setContentsMargins(5, 5, 5, 5)
        
        self.boton_finalizar_venta = QPushButton("Finalizar Venta")
        self.boton_finalizar_venta.setFont(QFont('Arial', 10, QFont.Bold))
        self.boton_finalizar_venta.setStyleSheet("background: #8A7F68; color: white;")
        self.boton_finalizar_venta.clicked.connect(self.finalizar_venta)
        
        layout_botones.addWidget(self.boton_finalizar_venta)
        parent_layout.addLayout(layout_botones)

    # ======================= FUNCIONALIDADES =======================
    def actualizar_tabla(self, datos=None):
        """Actualiza la tabla con los datos del inventario, incluyendo productos con stock cero."""
        self.tabla.setRowCount(0)
        
        datos_a_mostrar = datos if datos is not None else self.datos
        
        for nombre, detalles in datos_a_mostrar.items():
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            
            item_nombre = QTableWidgetItem(nombre)
            item_precio = QTableWidgetItem(detalles["Cantidad"])
            item_stock = QTableWidgetItem(str(detalles["Stock"]))
            
            # Resaltar en rojo si no hay stock
            if int(detalles["Stock"]) <= 0:
                item_stock.setForeground(QColor("red"))
                item_nombre.setForeground(QColor("red"))
            
            for item in [item_nombre, item_precio, item_stock]:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            
            self.tabla.setItem(row_position, 0, item_nombre)
            self.tabla.setItem(row_position, 1, item_precio)
            self.tabla.setItem(row_position, 2, item_stock)

    def buscar_en_tiempo_real(self):
        """Busca artículos mientras se escribe en el campo de búsqueda."""
        texto_busqueda = self.input_buscar.text().strip().lower()
        
        if not texto_busqueda:
            self.actualizar_tabla()
            return
        
        resultados = {}
        for nombre, detalles in self.datos.items():
            if texto_busqueda in nombre.lower():
                resultados[nombre] = detalles
        
        self.actualizar_tabla(resultados)

    def actualizar_precio_venta(self):
        """Actualiza el precio unitario cuando se escribe el nombre del producto."""
        nombre_producto = self.input_producto_venta.text().strip()
        
        # Buscar coincidencia insensible a mayúsculas/minúsculas
        for nombre in self.datos.keys():
            if nombre.lower() == nombre_producto.lower():
                precio = self.datos[nombre]["Cantidad"]
                self.input_precio_venta.setText(precio)
                self.validar_stock_venta()  # Validar stock al cambiar producto
                return
        
        # Si no se encuentra coincidencia
        self.input_precio_venta.clear()
        self.input_total_producto.clear()

    def validar_stock_venta(self):
        """Valida el stock y muestra 'Sin Stock' si es cero."""
        nombre_producto = self.input_producto_venta.text().strip()
        cantidad_texto = self.input_cantidad_venta.text().strip()
        
        if not nombre_producto:
            return
        
        # Buscar producto (insensible a mayúsculas/minúsculas)
        producto_encontrado = None
        for nombre in self.datos.keys():
            if nombre.lower() == nombre_producto.lower():
                producto_encontrado = nombre
                break
        
        if not producto_encontrado:
            self.input_cantidad_venta.setStyleSheet("border: 1px solid red; color: red;")
            self.input_total_producto.setText("Producto no existe")
            self.input_total_producto.setStyleSheet("color: red;")
            return
        
        stock_actual = int(self.datos[producto_encontrado]["Stock"])
        
        # Mostrar "Sin Stock" si stock = 0
        if stock_actual <= 0:
            self.input_cantidad_venta.setStyleSheet("border: 1px solid red; color: red;")
            self.input_total_producto.setText("Sin Stock")
            self.input_total_producto.setStyleSheet("color: red;")
            return
        
        # Validar cantidad ingresada
        try:
            cantidad = int(cantidad_texto) if cantidad_texto else 0
        except ValueError:
            self.input_cantidad_venta.setStyleSheet("border: 1px solid red; color: red;")
            return
        
        if cantidad <= 0:
            self.input_cantidad_venta.setStyleSheet("border: 1px solid red; color: red;")
            self.input_total_producto.setText("Cantidad inválida")
            self.input_total_producto.setStyleSheet("color: red;")
        elif cantidad > stock_actual:
            self.input_cantidad_venta.setStyleSheet("border: 1px solid red; color: red;")
            self.input_total_producto.setText(f"Stock insuficiente (max: {stock_actual})")
            self.input_total_producto.setStyleSheet("color: red;")
        else:
            self.input_cantidad_venta.setStyleSheet("")
            self.calcular_total_producto()

    def calcular_total_producto(self):
        """Calcula el total para el producto actual."""
        try:
            if not self.input_precio_venta.text() or not self.input_cantidad_venta.text():
                return
                
            precio_texto = ''.join(c for c in self.input_precio_venta.text() if c.isdigit() or c == '.')
            precio = float(precio_texto) if precio_texto else 0
            
            cantidad = int(self.input_cantidad_venta.text()) if self.input_cantidad_venta.text() else 0
            
            if cantidad <= 0:
                return
                
            total = precio * cantidad
            self.input_total_producto.setText(f"{total:,.0f} COP")
            self.input_total_producto.setStyleSheet("")
        except ValueError:
            self.input_total_producto.clear()

    def calcular_cambio(self):
        """Calcula el cambio a devolver al cliente."""
        try:
            if not self.input_total_venta.text() or not self.input_dinero_recibido.text():
                self.input_cambio.clear()
                return
            
            total_venta = float(''.join(c for c in self.input_total_venta.text() if c.isdigit() or c == '.'))
            dinero_recibido = float(''.join(c for c in self.input_dinero_recibido.text() if c.isdigit() or c == '.'))
            
            if dinero_recibido < total_venta:
                self.input_cambio.setText("Fondos insuficientes")
                self.input_cambio.setStyleSheet("color: red;")
            else:
                cambio = dinero_recibido - total_venta
                self.input_cambio.setText(f"{cambio:,.0f} COP")
                self.input_cambio.setStyleSheet("color: green;")
        except ValueError:
            self.input_cambio.clear()

    def agregar_a_venta(self):
        """Agrega un producto a la venta actual."""
        producto_ingresado = self.input_producto_venta.text().strip()
        precio_texto = self.input_precio_venta.text().strip()
        cantidad_texto = self.input_cantidad_venta.text().strip()
        total_texto = self.input_total_producto.text().strip()
        
        if not producto_ingresado or not precio_texto or not cantidad_texto or not total_texto:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios para agregar a la venta.")
            return
        
        # Buscar coincidencia insensible a mayúsculas/minúsculas
        producto_encontrado = None
        for nombre in self.datos.keys():
            if nombre.lower() == producto_ingresado.lower():
                producto_encontrado = nombre
                break
        
        if not producto_encontrado:
            QMessageBox.warning(self, "Advertencia", "El producto no existe en el inventario.")
            return
        
        try:
            precio = float(''.join(c for c in precio_texto if c.isdigit() or c == '.'))
            cantidad = int(cantidad_texto)
            if cantidad <= 0:
                QMessageBox.warning(self, "Advertencia", "La cantidad debe ser un número entero positivo.")
                return
            
            total = float(''.join(c for c in total_texto if c.isdigit() or c == '.'))
            stock_actual = int(self.datos[producto_encontrado]["Stock"])
            
            if cantidad > stock_actual:
                QMessageBox.warning(self, "Advertencia", f"No hay suficiente stock. Stock actual: {stock_actual}")
                return
                
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Datos inválidos: {str(e)}")
            return
        
        item_venta = {
            "producto": producto_encontrado,
            "precio": f"{precio:,.0f} COP",
            "cantidad": cantidad,
            "total": total
        }
        
        self.venta_actual.append(item_venta)
        self.actualizar_tabla_venta()
        
        self.input_producto_venta.clear()
        self.input_precio_venta.clear()
        self.input_cantidad_venta.clear()
        self.input_total_producto.clear()

    def actualizar_tabla_venta(self):
        """Actualiza la tabla de venta con los productos agregados."""
        self.tabla_venta.setRowCount(0)
        self.total_venta = 0
        
        for item in self.venta_actual:
            row_position = self.tabla_venta.rowCount()
            self.tabla_venta.insertRow(row_position)
            
            self.tabla_venta.setItem(row_position, 0, QTableWidgetItem(item["producto"]))
            self.tabla_venta.setItem(row_position, 1, QTableWidgetItem(item["precio"]))
            self.tabla_venta.setItem(row_position, 2, QTableWidgetItem(str(item["cantidad"])))
            self.tabla_venta.setItem(row_position, 3, QTableWidgetItem(f"{item['total']:,.0f} COP"))
            
            self.total_venta += item["total"]
        
        self.input_total_venta.setText(f"{self.total_venta:,.0f} COP")
        self.input_dinero_recibido.clear()
        self.input_cambio.clear()

    def finalizar_venta(self):
        """Finaliza la venta y actualiza el inventario."""
        if not self.venta_actual:
            QMessageBox.warning(self, "Advertencia", "No hay productos en la venta.")
            return
        
        try:
            dinero_recibido_text = ''.join(c for c in self.input_dinero_recibido.text() if c.isdigit() or c == '.')
            if not dinero_recibido_text:
                QMessageBox.warning(self, "Advertencia", "Ingrese el monto recibido del cliente.")
                return
            dinero_recibido = float(dinero_recibido_text)
            if dinero_recibido < self.total_venta:
                QMessageBox.warning(self, "Advertencia", "El monto recibido es menor al total de la venta.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Monto recibido inválido.")
            return
        
        reply = QMessageBox.question(
            self, "Confirmar Venta",
            f"¿Confirmar venta por un total de {self.total_venta:,.0f} COP?\n"
            f"Recibido: {dinero_recibido:,.0f} COP\n"
            f"Cambio: {dinero_recibido - self.total_venta:,.0f} COP",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for item in self.venta_actual:
                producto = item["producto"]
                cantidad = item["cantidad"]
                self.datos[producto]["Stock"] = str(int(self.datos[producto]["Stock"]) - cantidad)
            
            self.guardar_datos()
            self.venta_actual = []
            self.total_venta = 0
            self.tabla_venta.setRowCount(0)
            self.input_total_venta.clear()
            self.input_dinero_recibido.clear()
            self.input_cambio.clear()
            self.actualizar_tabla()
            self.actualizar_completer()
            
            QMessageBox.information(
                self, "Venta Exitosa",
                f"Venta finalizada por {self.total_venta:,.0f} COP\n"
                f"Cambio entregado: {dinero_recibido - self.total_venta:,.0f} COP"
            )

    def cargar_datos_seleccionados(self):
        """Carga los datos del artículo seleccionado en la tabla a los campos de edición."""
        selected_items = self.tabla.selectedItems()
        
        if selected_items:
            nombre = selected_items[0].text()
            if nombre in self.datos:
                articulo = self.datos[nombre]
                self.input_nombre.setText(nombre)
                self.input_precio.setText(articulo["Cantidad"])
                self.input_stock.setText(str(articulo["Stock"]))

    def agregar_actualizar_articulo(self):
        """Agrega o actualiza un artículo en el inventario."""
        nombre = self.input_nombre.text().strip()
        precio = self.input_precio.text().strip()
        stock = self.input_stock.text().strip()
        
        if not nombre or not precio or not stock:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return
        
        try:
            int(stock)
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "El stock debe ser un número entero.")
            return
        
        self.datos[nombre] = {
            "Cantidad": precio,
            "Stock": int(stock)
        }
        
        self.guardar_datos()
        self.actualizar_tabla()
        self.limpiar_campos()
        self.actualizar_completer()
        
        QMessageBox.information(self, "Éxito", f"Artículo '{nombre}' actualizado en el inventario.")

    def eliminar_articulo(self):
        """Elimina el artículo seleccionado."""
        selected_items = self.tabla.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un artículo para eliminar.")
            return
        
        nombre = selected_items[0].text()
        
        reply = QMessageBox.question(
            self, "Confirmar",
            f"¿Está seguro que desea eliminar el artículo '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self.datos[nombre]
            self.guardar_datos()
            self.actualizar_tabla()
            self.limpiar_campos()
            self.actualizar_completer()
            QMessageBox.information(self, "Éxito", f"Artículo '{nombre}' eliminado del inventario.")

    def limpiar_campos(self):
        """Limpia todos los campos de entrada."""
        self.input_nombre.clear()
        self.input_precio.clear()
        self.input_stock.clear()
        self.tabla.clearSelection()

    def mostrar_todo(self):
        """Muestra todos los artículos en la tabla."""
        self.input_buscar.clear()
        self.actualizar_tabla()

    def actualizar_completer(self):
        """Actualiza el autocompletado en el campo de producto para las ventas."""
        completer = QCompleter(list(self.datos.keys()))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.input_producto_venta.setCompleter(completer)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    ventana = InventarioApp()
    ventana.show()
    app.exec_()