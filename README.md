> [!HorarioClases]
> 
HorarioClases es una aplicación de escritorio diseñada para gestionar horarios académicos, tareas y notificaciones de vencimiento. Permite a los usuarios organizar materias, asignar horarios con profesores, agregar tareas con fechas de entrega y recibir notificaciones cuando estas estén próximas a vencer. La interfaz gráfica está construida con PyQt5 y utiliza SQLite como base de datos local.

> [!Características]
>
- **Gestión de materias**: Agrega materias fácilmente sin necesidad de asignar horarios de inmediato.
- **Horarios personalizados**: Asigna días, horas de inicio/fin y profesores a cada materia.
- **Tareas con notificaciones**: Programa tareas con fecha y hora de entrega; recibe notificaciones 30 minutos antes del vencimiento.
- **Eliminación de tareas**: Borra tareas completadas sin afectar materias ni horarios.
- **Reloj en tiempo real**: Muestra la hora actual de Colombia (UTC-5) en formato 24h junto con la fecha.
- **Interfaz intuitiva**: Botones con íconos modernos (usando `qtawesome`) para una experiencia visual limpia.
- **Sección "Acerca de"**: Información del desarrollador, contacto y licencia en un diálogo accesible desde la interfaz.
- **Exportable**: Compatible con Linux y Windows como ejecutable standalone mediante PyInstaller.

> [!Tecnologías utilizadas]
> 
- **Python 3.x**: Lenguaje principal del proyecto.
- **PyQt5**: Biblioteca para la interfaz gráfica (incluye `QtWidgets`, `QtGui`, `QtCore` para widgets, colores, íconos, temporizadores, etc.).
- **SQLite3**: Biblioteca estándar de Python para la base de datos ligera que almacena materias, horarios y tareas.
- **Plyer**: Para enviar notificaciones nativas al sistema operativo.
- **QtAwesome**: Proporciona íconos modernos de FontAwesome (ej. tuerca para "Acerca de").
- **Datetime**: Biblioteca estándar de Python para manejar fechas y horas, ajustada a la zona horaria de Colombia (UTC-5).
- **PyInstaller**: Herramienta opcional para empaquetar la aplicación en ejecutables independientes.

> [!Estructura del proyecto]
> 
>/HorarioClases/
  - ├── datos/
  - │   └── horario.db
  - ├── utilidades/
  - │   └── notificaciones.py
  - ├── modelos/
  - │   └── acerca.py
  - ├── interfaz_grafica.py
  - ├── README.md
  - └── requirements.txt
>
> [Requisitos]
  - Python 3.6 o superior
  - Dependencias (ver `requirements.txt`):
  - PyQt5==5.15.9
  - plyer==2.1.0
  - qtawesome==1.3.1


> [!Instalación]
1. **Clona el repositorio**:

    > git clone https://github.com/YsdCastro24/HorarioClases.git
    > cd HorarioClases

2. **Crea un entorno virtual (opcional pero recomendado)**:

    > python -m venv .venv
    > source .venv/bin/activate  # Linux
    > .venv\Scripts\activate     # Windows

3. **Instala las dependencias**:
    > pip install -r requirements.txt

4. **Ejecuta la aplicación**:
    > python interfaz_grafica.py

> [!Uso]
> 
  - **Agregar Materia**: Usa el botón "Agregar Materia" para crear una nueva materia.
  - **Asignar Horario**: Selecciona una materia y define su día, hora y profesor.
  - **Agregar Tarea**: Elige una materia, añade una descripción, fecha y hora de entrega.
  - **Eliminar Tarea**: Selecciona una fila en la tabla y usa "Eliminar Tarea" para borrar una tarea específica.
  - **Acerca de**: Haz clic en el ícono de tuerca para ver información del desarrollador.
>
> [!Contribuciones]
>¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto:
>
> Haz un fork del repositorio.
  - Crea una rama para tu cambio (git checkout -b mejora-nueva-funcion).
  - Realiza tus cambios y haz commit (git commit -m "Añadí nueva función").
  - Sube los cambios (git push origin mejora-nueva-funcion).
  - Abre un Pull Request.
>

> [!Autor]
  - **Yesid A. Castro Renteria**
  - **Correo**: ingenieroyesidcasstro08@gmail.com
  - **GitHub**: github.com/YsdCastro24
>
Licencia
© 2025 Yesid Castro. Todos los derechos reservados. Este software no puede ser distribuido, copiado o modificado sin autorización expresa del autor.





