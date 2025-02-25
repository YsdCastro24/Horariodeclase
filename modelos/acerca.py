
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class AcercaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("QDialog { background-color: #f0f0f0; } QLabel { font-size: 14px; }")

        layout = QVBoxLayout()

        # Información del software
        info = QLabel("""
        <h2>TaskSched Pro</h2>
        <b>Versión:</br> 1.0.0<br>
        <b>Desarrollador:</b> Yesid A. Castro Renteria<br>
        <b>Descripción:</b> Software diseñado para gestionar horarios y tareas académicas.<br>
        <b>Fecha de lanzamiento:</b> 24/02/2025
        """)
        layout.addWidget(info)

        # Información de contacto
        contacto = QLabel("""
        <h3>Contacto</h3>
        📧 <b>Correo:</b> ingenieroyesidcastro08@gmail.com<br>
        🌐 <b>Sitio web:</b> https://portafolio-yesid.vercel.app<br>
        📞 <b>Teléfono:</b> +573128631769<br>
        🔗 <b>Twitter:</b> @bartmusick<br>
        🔗 <b>GitHub:</b> github.com/YsdCastro24
        """)
        layout.addWidget(contacto)

        # Licencia
        licencia = QLabel("""
        <h3>Licencia</h3>
        © 2025 Yesid A. Castro Renteria. Todos los derechos reservados.<br>
        Este software no puede ser distribuido, copiado o modificado sin autorización.
        """)
        layout.addWidget(licencia)

        # Botón cerrar
        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.clicked.connect(self.accept)
        layout.addWidget(boton_cerrar)

        self.setLayout(layout)