from consulta_salas import Sala, Administrador

# Registrar y editar salas (Admin)
def registrar_sala(usuario_actual, nombre, ubicacion, capacidad, estado):
    if not isinstance(usuario_actual, Administrador):
        print("No autorizado: solo un administrador puede registrar salas.")
        return None

    nueva_sala = Sala(None, nombre, ubicacion, capacidad, estado)
    nueva_sala.guardar()

    return nueva_sala

def editar_sala(usuario_actual, id_sala, nombre, ubicacion, capacidad, estado):
    if not isinstance(usuario_actual, Administrador):
        print("No autorizado: solo un administrador puede editar salas.")
        return None

    # Creas el objeto con los nuevos datos
    sala = Sala(id_sala, nombre, ubicacion, capacidad, estado)
    
    try:
        # El método se encarga de verificar si el ID existe y actualizar
        sala.actualizar(id_sala)
        return sala
    except ValueError as e:
        print(e)
        return None