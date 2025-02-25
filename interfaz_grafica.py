import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, 
    QVBoxLayout, QHBoxLayout, QWidget, QDialog, QLineEdit, QLabel, QComboBox,
    QTimeEdit, QMessageBox, QHeaderView, QDateEdit
)
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QTime, QDate, QTimer, QSize
from datetime import datetime, timezone, timedelta
from utilidades.notificaciones import mostrar_notificacion
from modelos.acerca import AcercaDialog
import qtawesome as qta

class HorarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horario de Clases")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QTableWidget { background-color: white; alternate-background-color: #f9f9f9; border: 1px solid #d3d3d3; }
            QTableWidget::item { padding: 5px; }
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px 16px; font-size: 14px; margin: 4px 2px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
        """)

        # Tabla principal
        self.tabla_horario = QTableWidget(self)
        self.tabla_horario.setColumnCount(5)
        self.tabla_horario.setHorizontalHeaderLabels(["Materia", "Día", "Horario", "Profesor", "Tareas Pendientes"])
        self.tabla_horario.setAlternatingRowColors(True)
        self.tabla_horario.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Botones
        self.boton_agregar_materia = QPushButton("Agregar Materia", self)
        self.boton_agregar_materia.clicked.connect(self.abrir_formulario_materia)

        self.boton_agregar_horario = QPushButton("Asignar Horario", self)
        self.boton_agregar_horario.clicked.connect(self.abrir_formulario_horario)

        self.boton_agregar_tarea = QPushButton("Agregar Tarea", self)
        self.boton_agregar_tarea.clicked.connect(self.abrir_formulario_tarea)

        self.boton_eliminar_tarea = QPushButton("Eliminar Tarea", self)
        self.boton_eliminar_tarea.clicked.connect(self.eliminar_tarea)

         # Botón Acerca de con ícono de tuerca
        self.boton_acerca = QPushButton(self)
        self.boton_acerca.setIcon(qta.icon('fa5s.cog'))  # Ícono de tuerca de FontAwesome
        self.boton_acerca.setToolTip("Acerca de")
        self.boton_acerca.clicked.connect(self.mostrar_acerca)
        self.boton_acerca.setIconSize(QSize(24, 24))  # Tamaño personalizado del ícono
        self.boton_acerca.setIcon(qta.icon('fa5s.cog', color='white'))

        # Reloj
        self.reloj = QLabel(self)
        self.reloj.setAlignment(Qt.AlignCenter)
        self.reloj.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.actualizar_reloj()
        reloj_timer = QTimer(self)
        reloj_timer.timeout.connect(self.actualizar_reloj)
        reloj_timer.start(1000)

        # Layout
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_agregar_materia)
        layout_botones.addWidget(self.boton_agregar_horario)
        layout_botones.addWidget(self.boton_agregar_tarea)
        layout_botones.addWidget(self.boton_eliminar_tarea)
        layout_botones.addWidget(self.boton_acerca)

        layout = QVBoxLayout()
        layout.addWidget(self.reloj)
        layout.addWidget(self.tabla_horario)
        layout.addLayout(layout_botones)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Cargar datos
        self.cargar_datos()

        # Temporizador para verificar tareas
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.verificar_tareas)
        self.timer.start(60000)

    def cargar_datos(self):
        conexion = sqlite3.connect('datos/horario.db')
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT m.nombre, h.dia, h.hora_inicio || ' - ' || h.hora_fin, h.profesor,
                   (SELECT COUNT(*) FROM tareas WHERE materia_id = m.id)
            FROM materias m
            LEFT JOIN horarios h ON m.id = h.materia_id
            ORDER BY h.dia, h.hora_inicio
        """)
        datos = cursor.fetchall()
        conexion.close()

        self.tabla_horario.setRowCount(len(datos))
        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                item = QTableWidgetItem(str(valor) if valor else "")
                item.setTextAlignment(Qt.AlignCenter)
                if j == 4 and int(valor or 0) > 0:
                    item.setBackground(QColor(255, 200, 200))
                self.tabla_horario.setItem(i, j, item)

    def verificar_tareas(self):
        ahora = datetime.now(timezone(timedelta(hours=-5)))  # UTC-5 Colombia
        conexion = sqlite3.connect('datos/horario.db')
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT m.nombre, t.descripcion, t.fecha_entrega, t.hora_entrega
            FROM tareas t
            JOIN materias m ON t.materia_id = m.id
        """)
        tareas = cursor.fetchall()
        conexion.close()

        for materia, descripcion, fecha, hora in tareas:
            fecha_hora_entrega = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone(timedelta(hours=-5)))
            diferencia = fecha_hora_entrega - ahora
            minutos_restantes = diferencia.total_seconds() / 60
            if 0 < minutos_restantes <= 30:
                mostrar_notificacion(
                    f"Tarea Próxima: {materia}",
                    f"{descripcion} - Entrega: {fecha} {hora}"
                )

    def eliminar_tarea(self):
        fila_seleccionada = self.tabla_horario.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Error", "Por favor, seleccione una fila con una materia que tenga tareas.")
            return

        materia = self.tabla_horario.item(fila_seleccionada, 0).text()
        tareas_pendientes = int(self.tabla_horario.item(fila_seleccionada, 4).text() or 0)

        if tareas_pendientes == 0:
            QMessageBox.information(self, "Sin tareas", "No hay tareas pendientes para esta materia.")
            return

        conexion = sqlite3.connect('datos/horario.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM materias WHERE nombre = ?", (materia,))
        materia_id = cursor.fetchone()[0]
        cursor.execute("SELECT id, descripcion FROM tareas WHERE materia_id = ?", (materia_id,))
        tareas = cursor.fetchall()

        if tareas:
            dialogo = QDialog(self)
            dialogo.setWindowTitle("Eliminar Tarea")
            layout = QVBoxLayout()
            label = QLabel("Seleccione la tarea a eliminar:")
            combo_tareas = QComboBox()
            combo_tareas.addItems([t[1] for t in tareas])
            boton_confirmar = QPushButton("Eliminar")
            boton_confirmar.clicked.connect(lambda: self.confirmar_eliminar_tarea(tareas[combo_tareas.currentIndex()][0], dialogo))

            layout.addWidget(label)
            layout.addWidget(combo_tareas)
            layout.addWidget(boton_confirmar)
            dialogo.setLayout(layout)
            dialogo.exec_()

        conexion.close()

    def confirmar_eliminar_tarea(self, tarea_id, dialogo):
        conexion = sqlite3.connect('datos/horario.db')
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        conexion.commit()
        conexion.close()
        dialogo.accept()
        self.cargar_datos()

    def actualizar_reloj(self):
        colombia_tz = timezone(timedelta(hours=-5))
        hora_colombia = datetime.now(colombia_tz).strftime("%H:%M:%S - %Y-%m-%d")
        self.reloj.setText(f"Hora Colombia: {hora_colombia}")

    def mostrar_acerca(self):
        dialogo = AcercaDialog(self)
        dialogo.exec_()

    def abrir_formulario_materia(self):
        dialogo = FormularioMateria(self)
        if dialogo.exec_():
            self.cargar_datos()

    def abrir_formulario_horario(self):
        dialogo = FormularioHorario(self)
        if dialogo.exec_():
            self.cargar_datos()

    def abrir_formulario_tarea(self):
        dialogo = FormularioTarea(self)
        if dialogo.exec_():
            self.cargar_datos()

class FormularioMateria(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Materia")
        self.setGeometry(300, 300, 400, 150)
        self.setStyleSheet("""
            QDialog { background-color: #f0f0f0; }
            QLabel { font-weight: bold; }
            QLineEdit, QComboBox, QTimeEdit { padding: 5px; border: 1px solid #ccc; border-radius: 3px; }
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px 16px; font-size: 14px; margin: 4px 2px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
        """)

        layout = QVBoxLayout()
        self.label_nombre = QLabel("Nombre de la Materia:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setFocus()
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.input_nombre)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_materia)
        layout.addWidget(self.boton_guardar)

        self.setLayout(layout)

    def guardar_materia(self):
        nombre_materia = self.input_nombre.text().strip()
        if nombre_materia:
            conexion = sqlite3.connect('datos/horario.db')
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO materias (nombre) VALUES (?)", (nombre_materia,))
            conexion.commit()
            conexion.close()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese el nombre de la materia.")

class FormularioHorario(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Asignar Horario")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("""
            QDialog { background-color: #f0f0f0; }
            QLabel { font-weight: bold; }
            QLineEdit, QComboBox, QTimeEdit { padding: 5px; border: 1px solid #ccc; border-radius: 3px; }
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px 16px; font-size: 14px; margin: 4px 2px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
        """)

        layout = QVBoxLayout()

        self.label_materia = QLabel("Materia:")
        self.combo_materia = QComboBox()
        self.combo_materia.setEditable(False)
        self.cargar_materias()
        self.combo_materia.setFocus()
        layout.addWidget(self.label_materia)
        layout.addWidget(self.combo_materia)

        self.label_dia = QLabel("Día de la semana:")
        self.combo_dia = QComboBox()
        self.combo_dia.addItems(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
        layout.addWidget(self.label_dia)
        layout.addWidget(self.combo_dia)

        self.label_hora_inicio = QLabel("Hora de inicio:")
        self.time_inicio = QTimeEdit()
        self.time_inicio.setDisplayFormat("HH:mm")
        layout.addWidget(self.label_hora_inicio)
        layout.addWidget(self.time_inicio)

        self.label_hora_fin = QLabel("Hora de fin:")
        self.time_fin = QTimeEdit()
        self.time_fin.setDisplayFormat("HH:mm")
        layout.addWidget(self.label_hora_fin)
        layout.addWidget(self.time_fin)

        self.label_profesor = QLabel("Profesor:")
        self.input_profesor = QLineEdit()
        layout.addWidget(self.label_profesor)
        layout.addWidget(self.input_profesor)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_horario)
        layout.addWidget(self.boton_guardar)

        self.setLayout(layout)

    def cargar_materias(self):
        conexion = sqlite3.connect('datos/horario.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM materias")
        materias = cursor.fetchall()
        conexion.close()
        self.combo_materia.addItems([materia[0] for materia in materias])

    def guardar_horario(self):
        materia = self.combo_materia.currentText()
        dia = self.combo_dia.currentText()
        hora_inicio = self.time_inicio.time().toString("HH:mm")
        hora_fin = self.time_fin.time().toString("HH:mm")
        profesor = self.input_profesor.text().strip()

        if materia and dia and hora_inicio and hora_fin and profesor:
            conexion = sqlite3.connect('datos/horario.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM materias WHERE nombre = ?", (materia,))
            materia_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO horarios (materia_id, dia, hora_inicio, hora_fin, profesor) VALUES (?, ?, ?, ?, ?)",
                           (materia_id, dia, hora_inicio, hora_fin, profesor))
            conexion.commit()
            conexion.close()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

class FormularioTarea(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Tarea")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("""
            QDialog { background-color: #f0f0f0; }
            QLabel { font-weight: bold; }
            QLineEdit, QComboBox, QDateEdit, QTimeEdit { padding: 5px; border: 1px solid #ccc; border-radius: 3px; }
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px 16px; font-size: 14px; margin: 4px 2px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
        """)

        layout = QVBoxLayout()

        self.label_materia = QLabel("Materia:")
        self.combo_materia = QComboBox()
        self.combo_materia.setEditable(False)
        self.cargar_materias()
        self.combo_materia.setFocus()
        layout.addWidget(self.label_materia)
        layout.addWidget(self.combo_materia)

        self.label_descripcion = QLabel("Descripción de la tarea:")
        self.input_descripcion = QLineEdit()
        layout.addWidget(self.label_descripcion)
        layout.addWidget(self.input_descripcion)

        self.label_fecha = QLabel("Fecha de entrega:")
        self.date_entrega = QDateEdit()
        self.date_entrega.setCalendarPopup(True)
        self.date_entrega.setDate(QDate.currentDate())
        layout.addWidget(self.label_fecha)
        layout.addWidget(self.date_entrega)

        self.label_hora = QLabel("Hora de entrega:")
        self.time_entrega = QTimeEdit()
        self.time_entrega.setDisplayFormat("HH:mm")
        layout.addWidget(self.label_hora)
        layout.addWidget(self.time_entrega)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_tarea)
        layout.addWidget(self.boton_guardar)

        self.setLayout(layout)

    def cargar_materias(self):
        conexion = sqlite3.connect('datos/horario.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM materias")
        materias = cursor.fetchall()
        conexion.close()
        self.combo_materia.addItems([materia[0] for materia in materias])

    def guardar_tarea(self):
        materia = self.combo_materia.currentText()
        descripcion = self.input_descripcion.text().strip()
        fecha_entrega = self.date_entrega.date().toString("yyyy-MM-dd")
        hora_entrega = self.time_entrega.time().toString("HH:mm")

        if materia and descripcion and fecha_entrega and hora_entrega:
            conexion = sqlite3.connect('datos/horario.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM materias WHERE nombre = ?", (materia,))
            materia_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO tareas (materia_id, descripcion, fecha_entrega, hora_entrega) VALUES (?, ?, ?, ?)",
                           (materia_id, descripcion, fecha_entrega, hora_entrega))
            conexion.commit()
            conexion.close()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    ventana = HorarioApp()
    ventana.show()
    app.exec_()