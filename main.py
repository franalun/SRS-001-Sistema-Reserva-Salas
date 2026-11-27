from consulta_salas import Sala

def mostrar_salas():
    salas = Sala.buscar_todos()

    print('===== Listado de salas =====')

    if len(salas) == 0:
        print('No hay salas registradas.')
        return
    
    for sala in salas:
        id_sala = sala.obtener_id()
        nombre = sala.obtener_nombre()
        ubicacion = sala.obtener_ubicacion()
        capacidad = sala.obtener_capacidad()
        estado = sala.obtener_estado()

        print(f'ID: {id_sala}')
        print(f'Nombre: {nombre}')
        print(f'Ubicación: {ubicacion}')
        print(f'Capacidad: {capacidad}')
        print(f'Estado: {estado}')
        print('-------------------------')
if __name__ == '__main__':
    mostrar_salas()