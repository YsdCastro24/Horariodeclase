from PyQt5.QtWidgets import QApplication
from interfaz_grafica import HorarioApp

if __name__ == "__main__":
    app = QApplication([])
    ventana = HorarioApp()
    ventana.show()
    app.exec_()
