from plyer import notification

def mostrar_notificacion(titulo, mensaje):
    notification.notify(
        title=titulo,
        message=mensaje,
        timeout=10  # Duración de la notificación en segundos
    )