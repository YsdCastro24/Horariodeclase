from plyer import notification

def mostrar_notificacion(titulo, mensaje):
    notification.notify(
        title=titulo,
        message=mensaje,
        timeout=20 
    )