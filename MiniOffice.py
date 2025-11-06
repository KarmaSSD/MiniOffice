from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QToolBar, QLabel, QMessageBox,
    QFileDialog, QColorDialog, QFontDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QDockWidget, QDialog
)
from PySide6.QtGui import (
    QAction, QKeySequence, QIcon, QTextCursor, QTextDocument,
    QFont, QTextCharFormat, QColor
)
from PySide6.QtCore import Qt
import os;


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini Word")
        self.resize(900, 600)

        # Editor de texto
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("QTextEdit { background-color: white; color: black; }")
        self.text_edit.textChanged.connect(self.al_cambiar_texto)


        # Formato predeterminado
        self.formato_predeterminado = QTextCharFormat()
        self.formato_predeterminado.setForeground(QColor("black"))
        self.formato_predeterminado.setFont(QFont("Arial", 10))
        self.text_edit.setCurrentCharFormat(self.formato_predeterminado)
        

        # Reaplicar formato despues de deshacer/rehacer
        self.text_edit.undoAvailable.connect(self.reaplicar_formato_predeterminado)
        self.text_edit.redoAvailable.connect(self.reaplicar_formato_predeterminado)

        # Barra de estado
        self.status = self.statusBar()
        self.label_palabras = QLabel("Palabras: 0")
        self.status.addPermanentWidget(self.label_palabras)

        # Menus
        self.crear_menus()

        # Barra de herramientas
        self.crear_toolbar()

        # Barra de formato
        self.crear_barra_formato()

        # Panel de busqueda
        self.panel_busqueda()

    # MENUS
    def crear_menus(self):
        # Menu Archivo
        menu_archivo = self.menuBar().addMenu("Archivo")

        self.accion_nuevo = QAction(QIcon.fromTheme("document-new"), "Nuevo", self)
        self.accion_nuevo.setShortcut(QKeySequence.New)
        self.accion_nuevo.triggered.connect(self.nuevo_documento)
        menu_archivo.addAction(self.accion_nuevo)

        self.accion_abrir = QAction(QIcon.fromTheme("document-open"), "Abrir", self)
        self.accion_abrir.setShortcut(QKeySequence.Open)
        self.accion_abrir.triggered.connect(self.abrir_documento)
        menu_archivo.addAction(self.accion_abrir)

        self.accion_guardar = QAction(QIcon.fromTheme("document-save"), "Guardar", self)
        self.accion_guardar.setShortcut(QKeySequence.Save)
        self.accion_guardar.triggered.connect(self.guardar_documento)
        menu_archivo.addAction(self.accion_guardar)

        menu_archivo.addSeparator()

        self.accion_salir = QAction(QIcon.fromTheme("application-exit"), "Salir", self)
        self.accion_salir.setShortcut("Ctrl+Q")
        self.accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(self.accion_salir)

        # Menu Editar
        menu_editar = self.menuBar().addMenu("Editar")

        self.accion_deshacer = QAction(QIcon.fromTheme("edit-undo"), "Deshacer", self)
        self.accion_deshacer.setShortcut(QKeySequence.Undo)
        self.accion_deshacer.triggered.connect(self.text_edit.undo)
        menu_editar.addAction(self.accion_deshacer)

        self.accion_rehacer = QAction(QIcon.fromTheme("edit-redo"), "Rehacer", self)
        self.accion_rehacer.setShortcut(QKeySequence.Redo)
        self.accion_rehacer.triggered.connect(self.text_edit.redo)
        menu_editar.addAction(self.accion_rehacer)

        menu_editar.addSeparator()

        self.accion_cortar = QAction(QIcon.fromTheme("edit-cut"), "Cortar", self)
        self.accion_cortar.setShortcut(QKeySequence.Cut)
        self.accion_cortar.triggered.connect(self.text_edit.cut)
        menu_editar.addAction(self.accion_cortar)

        self.accion_copiar = QAction(QIcon.fromTheme("edit-copy"), "Copiar", self)
        self.accion_copiar.setShortcut(QKeySequence.Copy)
        self.accion_copiar.triggered.connect(self.text_edit.copy)
        menu_editar.addAction(self.accion_copiar)

        self.accion_pegar = QAction(QIcon.fromTheme("edit-paste"), "Pegar", self)
        self.accion_pegar.setShortcut(QKeySequence.Paste)
        self.accion_pegar.triggered.connect(self.text_edit.paste)
        menu_editar.addAction(self.accion_pegar)

        menu_editar.addSeparator()

        self.accion_buscar = QAction(QIcon.fromTheme("edit-find"), "Buscar / Reemplazar", self)
        self.accion_buscar.setShortcut("Ctrl+F")
        self.accion_buscar.triggered.connect(self.mostrar_panel_busqueda)
        menu_editar.addAction(self.accion_buscar)

    # TOOLBAR
    def crear_toolbar(self):
        toolbar = QToolBar("Barra principal")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        toolbar.addAction(self.accion_nuevo)
        toolbar.addAction(self.accion_abrir)
        toolbar.addAction(self.accion_guardar)

        toolbar.addSeparator()

        toolbar.addAction(self.accion_deshacer)
        toolbar.addAction(self.accion_rehacer)

        toolbar.addSeparator()

        toolbar.addAction(self.accion_cortar)
        toolbar.addAction(self.accion_copiar)
        toolbar.addAction(self.accion_pegar)

        toolbar.addSeparator()

        toolbar.addAction(self.accion_buscar)


    # ----------- BARRA DE FORMATO -----------
    def crear_barra_formato(self):
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(5)

        self.btn_bold = QPushButton()
        self.btn_bold.setIcon(QIcon.fromTheme("format-text-bold"))
        self.btn_bold.setToolTip("Negrita (Ctrl+B)")
        self.btn_bold.setFixedSize(28, 28)
        self.btn_bold.setCheckable(True)
        self.btn_bold.clicked.connect(self.toggle_negrita)
        layout.addWidget(self.btn_bold)

        self.btn_italic = QPushButton()
        self.btn_italic.setIcon(QIcon.fromTheme("format-text-italic"))
        self.btn_italic.setToolTip("Cursiva (Ctrl+I)")
        self.btn_italic.setFixedSize(28, 28)
        self.btn_italic.setCheckable(True)
        self.btn_italic.clicked.connect(self.toggle_cursiva)
        layout.addWidget(self.btn_italic)

        self.btn_subrayado = QPushButton()
        self.btn_subrayado.setIcon(QIcon.fromTheme("format-text-underline"))
        self.btn_subrayado.setToolTip("Subrayado (Ctrl+U)")
        self.btn_subrayado.setFixedSize(28, 28)
        self.btn_subrayado.setCheckable(True)
        self.btn_subrayado.clicked.connect(self.toggle_subrayado)
        layout.addWidget(self.btn_subrayado)

        layout.addSpacing(10)

        # Rutas a los iconos
        self.icono_color_texto = os.path.join(os.path.dirname(__file__), "Images/colortexto.png")
        self.icono_color_fondo = os.path.join(os.path.dirname(__file__), "Images/colorfondo.png")

        # Boton color texto
        btn_color = QPushButton()
        btn_color.setIcon(QIcon(self.icono_color_texto))
        btn_color.setToolTip("Cambiar color de letra")
        btn_color.setFixedSize(28, 28)
        btn_color.clicked.connect(self.cambiar_color_letra)
        layout.addWidget(btn_color)

        # Boton color fondo
        btn_fondo = QPushButton()
        btn_fondo.setIcon(QIcon(self.icono_color_fondo))
        btn_fondo.setToolTip("Cambiar color de fondo")
        btn_fondo.setFixedSize(28, 28)
        btn_fondo.clicked.connect(self.cambiar_color_fondo)
        layout.addWidget(btn_fondo)

        btn_fuente = QPushButton()
        btn_fuente.setIcon(QIcon.fromTheme("preferences-desktop-font"))
        btn_fuente.setToolTip("Cambiar tipo de letra")
        btn_fuente.setFixedSize(28, 28)
        btn_fuente.clicked.connect(self.cambiar_fuente)
        layout.addWidget(btn_fuente)

        layout.addStretch()

        widget_central = QWidget()
        layout_central = QVBoxLayout(widget_central)
        layout_central.addWidget(contenedor)
        layout_central.addWidget(self.text_edit)
        layout_central.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(widget_central)

        self.text_edit.shortcut_bold = QAction(self)
        self.text_edit.shortcut_bold.setShortcut(QKeySequence.Bold)
        self.text_edit.shortcut_bold.triggered.connect(self.toggle_negrita)
        self.addAction(self.text_edit.shortcut_bold)

        self.text_edit.shortcut_italic = QAction(self)
        self.text_edit.shortcut_italic.setShortcut(QKeySequence.Italic)
        self.text_edit.shortcut_italic.triggered.connect(self.toggle_cursiva)
        self.addAction(self.text_edit.shortcut_italic)

        self.text_edit.shortcut_underline = QAction(self)
        self.text_edit.shortcut_underline.setShortcut(QKeySequence.Underline)
        self.text_edit.shortcut_underline.triggered.connect(self.toggle_subrayado)
        self.addAction(self.text_edit.shortcut_underline)

        # Estilo visual simple para botones activos
        style_checked = "QPushButton:checked { background-color: #d0eaff; }"
        self.btn_bold.setStyleSheet(style_checked)
        self.btn_italic.setStyleSheet(style_checked)
        self.btn_subrayado.setStyleSheet(style_checked)

        # Actualizar estado de los botones cuando cambia la posición del cursor
        self.text_edit.cursorPositionChanged.connect(self.actualizar_estado_botones_formato)
        # inicializar estado
        self.actualizar_estado_botones_formato()

    # ESTILOS DE TEXTO 
    def toggle_negrita(self):
        formato = QTextCharFormat()
        formato.setFontWeight(QFont.Bold if self.text_edit.fontWeight() != QFont.Bold else QFont.Normal)
        self.text_edit.mergeCurrentCharFormat(formato)

    def toggle_cursiva(self):
        formato = QTextCharFormat()
        formato.setFontItalic(not self.text_edit.fontItalic())
        self.text_edit.mergeCurrentCharFormat(formato)

    def toggle_subrayado(self):
        formato = QTextCharFormat()
        formato.setFontUnderline(not self.text_edit.fontUnderline())
        self.text_edit.mergeCurrentCharFormat(formato)

    # DOCUMENTO
    def actualizar_contador_palabras(self):
        texto = self.text_edit.toPlainText()
        self.label_palabras.setText(f"Palabras: {len(texto.split())}")

    def nuevo_documento(self):
        self.text_edit.clear()
        self.text_edit.setCurrentCharFormat(self.formato_predeterminado)
        self.status.showMessage("Nuevo documento creado", 2000)
        
    def abrir_documento(self):
        ruta = QFileDialog.getOpenFileName(self, "Abrir documento", "", "Text Files (*.txt);;All Files (*)")
        if ruta[0]:
            with open(ruta[0], "r", encoding="utf-8") as archivo:
                self.text_edit.setPlainText(archivo.read())
            self.status.showMessage(f"Documento '{ruta[0]}' abierto", 2000)

    def guardar_documento(self):
        ruta = QFileDialog.getSaveFileName(self, "Guardar documento", "", "Text Files (*.txt);;All Files (*)")
        if ruta[0]:
            with open(ruta[0], "w", encoding="utf-8") as archivo:
                archivo.write(self.text_edit.toPlainText())
            self.status.showMessage(f"Documento guardado en '{ruta[0]}'", 2000)

    # PERSONALIZACIÓN 
    def cambiar_color_letra(self):
        color = QColorDialog.getColor()
        if color.isValid():
            formato = QTextCharFormat()
            formato.setForeground(color)
            self.text_edit.mergeCurrentCharFormat(formato)
            self.formato_predeterminado.setForeground(color)
            self.status.showMessage(f"Color de letra cambiado a {color.name()}", 2000)

    def cambiar_color_fondo(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setStyleSheet(f"background-color: {color.name()};")
            self.status.showMessage(f"Color de fondo cambiado a {color.name()}", 2000)

    def cambiar_fuente(self):
        dialog = QFontDialog(self)
        dialog.setCurrentFont(self.text_edit.currentFont())
        if dialog.exec() != QDialog.Accepted:
            self.status.showMessage("Cambio de fuente cancelado.", 2000)
            return

        fuente = dialog.currentFont()
        if not isinstance(fuente, QFont):
            self.status.showMessage("Cambio de fuente cancelado.", 2000)
            return

        cursor = self.text_edit.textCursor()
        formato = QTextCharFormat()
        formato.setFont(fuente)

        if cursor.hasSelection():
            # Aplica la fuente a la selección
            cursor.beginEditBlock()
            cursor.mergeCharFormat(formato)
            self.text_edit.mergeCurrentCharFormat(formato)
            cursor.endEditBlock()
        else:
            # Establece la fuente por defecto para el documento y para el editor (nuevas inserciones)
            self.text_edit.document().setDefaultFont(fuente)
            self.text_edit.setCurrentFont(fuente)
            self.text_edit.setFont(fuente)

            # Asegura que el cursor tenga el formato actual (inserción)
            cur = self.text_edit.textCursor()
            cur.mergeCharFormat(formato)
            self.text_edit.setTextCursor(cur)

        # Actualiza el formato predeterminado guardado
        self.formato_predeterminado.setFont(fuente)
        self.status.showMessage(f"Fuente cambiada a {fuente.family()}", 2000)




    # MANTENER FORMATO TRAS DESHACER/REHACER 
    def reaplicar_formato_predeterminado(self):
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.formato_predeterminado)
        self.text_edit.mergeCurrentCharFormat(self.formato_predeterminado)

    # PANEL BUSCAR / REEMPLAZAR
    def panel_busqueda(self):
        self.dock_busqueda = QDockWidget("Buscar y Reemplazar", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_busqueda)
        self.dock_busqueda.hide()

        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout_buscar = QHBoxLayout()
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Texto a buscar...")
        layout_buscar.addWidget(self.input_buscar)

        self.btn_siguiente = QPushButton("Siguiente")
        self.btn_anterior = QPushButton("Anterior")
        self.btn_todas = QPushButton("Buscar todas")
        layout_buscar.addWidget(self.btn_anterior)
        layout_buscar.addWidget(self.btn_siguiente)
        layout_buscar.addWidget(self.btn_todas)
        layout.addLayout(layout_buscar)

        layout_reemplazar = QHBoxLayout()
        self.input_reemplazar = QLineEdit()
        self.input_reemplazar.setPlaceholderText("Reemplazar por...")
        layout_reemplazar.addWidget(self.input_reemplazar)

        self.btn_reemplazar = QPushButton("Reemplazar")
        self.btn_reemplazar_todo = QPushButton("Reemplazar todas")
        layout_reemplazar.addWidget(self.btn_reemplazar)
        layout_reemplazar.addWidget(self.btn_reemplazar_todo)
        layout.addLayout(layout_reemplazar)

        self.dock_busqueda.setWidget(widget)

        self.btn_siguiente.clicked.connect(self.buscar_siguiente)
        self.btn_anterior.clicked.connect(self.buscar_anterior)
        self.btn_todas.clicked.connect(self.buscar_todas)
        self.btn_reemplazar.clicked.connect(self.reemplazar)
        self.btn_reemplazar_todo.clicked.connect(self.reemplazar_todo)

    def mostrar_panel_busqueda(self):
        self.dock_busqueda.show()
        self.dock_busqueda.raise_()
        self.input_buscar.setFocus()

    # FUNCIONES DE BUSQUEDA Y REEMPLAZO
    def buscar_siguiente(self):
        texto = self.input_buscar.text().strip().lower()
        if not texto:
            return

        contenido = self.text_edit.toPlainText().lower()
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        idx = contenido.find(texto, pos)
        if idx == -1:
            idx = contenido.find(texto)
            if idx == -1:
                QMessageBox.information(self, "Buscar", f"No se encontraron más coincidencias de: {texto}")
                return
        cursor.setPosition(idx)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(texto))
        self.text_edit.setTextCursor(cursor)

    def buscar_anterior(self):
        texto = self.input_buscar.text().strip().lower()
        if not texto:
            return
        contenido = self.text_edit.toPlainText().lower()
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        idx = contenido.rfind(texto, 0, pos)
        if idx == -1:
            idx = contenido.rfind(texto)
            if idx == -1:
                QMessageBox.information(self, "Buscar", f"No se encontraron más coincidencias hacia atrás de: {texto}")
                return
        cursor.setPosition(idx)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(texto))
        self.text_edit.setTextCursor(cursor)

    def buscar_todas(self):
        texto = self.input_buscar.text().strip().lower()
        if not texto:
            return
        formato = QTextCharFormat()
        formato.setBackground(QColor("yellow"))
        selecciones = []
        contenido = self.text_edit.toPlainText().lower()
        start = 0
        count = 0
        while True:
            idx = contenido.find(texto, start)
            if idx == -1:
                break
            cursor = self.text_edit.textCursor()
            cursor.setPosition(idx)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(texto))
            extra = QTextEdit.ExtraSelection()
            extra.cursor = cursor
            extra.format = formato
            selecciones.append(extra)
            start = idx + len(texto)
            count += 1
        self.text_edit.setExtraSelections(selecciones)
        self.status.showMessage(f"{count} coincidencias encontradas.", 2000)

    def reemplazar(self):
        texto = self.input_buscar.text().strip().lower()
        reemplazo = self.input_reemplazar.text()
        if not texto:
            return
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            self.buscar_siguiente()
            cursor = self.text_edit.textCursor()
        if cursor.hasSelection() and cursor.selectedText().lower() == texto:
            cursor.insertText(reemplazo)
            self.buscar_siguiente()

    def reemplazar_todo(self):
        texto = self.input_buscar.text().strip().lower()
        reemplazo = self.input_reemplazar.text()
        if not texto:
            return
        contenido = self.text_edit.toPlainText()
        contenido_lower = contenido.lower()
        start = 0
        resultado = ""
        count = 0
        while True:
            idx = contenido_lower.find(texto, start)
            if idx == -1:
                resultado += contenido[start:]
                break
            resultado += contenido[start:idx] + reemplazo
            start = idx + len(texto)
            count += 1
        self.text_edit.setPlainText(resultado)
        self.status.showMessage(f"Se reemplazaron {count} ocurrencias de '{texto}'.", 2000)

    def al_cambiar_texto(self):
        # Actualiza el contador de palabras
        texto = self.text_edit.toPlainText()
        self.label_palabras.setText(f"Palabras: {len(texto.split())}")

        # Si el documento está vacío, restablece el formato predeterminado
        if not texto:
            self.asegurar_formato_insercion()

        # Si había resaltados de búsqueda, los limpia al modificar el texto
        if hasattr(self, "_tiene_resaltados") and self._tiene_resaltados:
            self.text_edit.setExtraSelections([])
            self._tiene_resaltados = False


    def asegurar_formato_insercion(self):
        # Reaplica el color y la fuente predeterminados como formato de inserción
        self.text_edit.blockSignals(True)

        # Aplica el color de texto por defecto
        self.text_edit.setTextColor(self.formato_predeterminado.foreground().color())

        # Aplica la fuente por defecto
        self.text_edit.setCurrentFont(self.formato_predeterminado.font())

        # Mezcla también el formato con el cursor actual
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.formato_predeterminado)
        self.text_edit.setTextCursor(cursor)

        # Establece el formato actual como el predeterminado
        self.text_edit.setCurrentCharFormat(self.formato_predeterminado)

        self.text_edit.blockSignals(False)


    def reaplicar_formato_predeterminado(self):
        # Llamado tras deshacer o rehacer para mantener el formato
        self.asegurar_formato_insercion()

    def actualizar_estado_botones_formato(self):
        # Actualiza el estado de los botones de formato (negrita, cursiva, subrayado)
        cursor = self.text_edit.textCursor()
        formato = cursor.charFormat()

        # Negrita
        self.btn_bold.setChecked(formato.fontWeight() == QFont.Bold)

        # Cursiva
        self.btn_italic.setChecked(formato.fontItalic())

        # Subrayado
        self.btn_subrayado.setChecked(formato.fontUnderline())

        # Actualiza el estilo de los botones según su estado
        for btn in [self.btn_bold, self.btn_italic, self.btn_subrayado]:
            if btn.isChecked():
                btn.setStyleSheet("QPushButton:checked { background-color: #d0eaff; }")
            else:
                btn.setStyleSheet("")


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()