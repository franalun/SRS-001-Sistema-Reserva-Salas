import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from consulta_salas import *
from conexion import Conexion
from admin_opc import registrar_sala, editar_sala

VENTANA_DIMENSIONES = '640x480'
usuario_tipo_actual = None
usuario_actual = None

def mostrar_ventana(tipo: str = 'info', mensaje: str = None, padre: tk.Tk = None):
    if mensaje is None:
        mensaje = 'Mensaje predeterminado'
    match tipo:
        case 'info':
            messagebox.showinfo('Información', mensaje, parent=padre)
        case 'error':
            messagebox.showerror('Error', mensaje, parent=padre)
        case 'advertencia':
            messagebox.showwarning('Advertencia', mensaje, parent=padre)

def ventana_login(ventana):
    contenedor_login = tk.Frame(ventana)
    contenedor_login.pack(expand=True)

    tk.Label(contenedor_login, text="Usuario").pack(pady=5)
    username_entry = tk.Entry(contenedor_login)
    username_entry.pack()

    tk.Label(contenedor_login, text="Contraseña").pack(pady=5)
    password_entry = tk.Entry(contenedor_login, show="*")
    password_entry.pack()

    def iniciar_sesion():
        global usuario_actual, usuario_tipo_actual
        username = username_entry.get().strip()
        password = password_entry.get()

        if not username or not password:
            mostrar_ventana("error", "Debe ingresar usuario y contraseña.", ventana)
            return

        try:
            usuario = Usuario.iniciar_sesion(username, password)
            if usuario is None:
                mostrar_ventana("error", "Usuario o contraseña incorrectos.", ventana)
                return

            usuario_actual = usuario
            if isinstance(usuario, Administrador):
                usuario_tipo_actual = "administrador"
            else:
                usuario_tipo_actual = "empleado"

            contenedor_login.destroy()  # Borra solo el formulario de login
            opciones_menu(ventana)      # Dibuja el menú en la misma ventana
        except Exception as e:
            mostrar_ventana("error", f"Error al iniciar sesión:\n{e}", ventana)

    tk.Button(contenedor_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=15)

def opciones_menu(ventana):
    ANCHO_BOTON = 30
    ALTO_BOTON = 2

    contenedor = tk.Frame(ventana)
    contenedor.pack(expand=True)

    tk.Label(contenedor, text=f"Bienvenido, {usuario_actual.obtener_nombre()}",
             font=("Arial", 14)).pack(pady=(0, 20))

    # Opciones disponibles para cualquier usuario con sesión iniciada
    tk.Button(contenedor, text="Ver salas disponibles", width=ANCHO_BOTON, height=ALTO_BOTON,
          command=ventana_salas).pack(pady=5)

    tk.Button(contenedor, text="Reservar sala", width=ANCHO_BOTON, height=ALTO_BOTON,
              command=lambda: print("Pendiente: reservar sala")).pack(pady=5)

    tk.Button(contenedor, text="Mis reservas", width=ANCHO_BOTON, height=ALTO_BOTON,
              command=lambda: print("Pendiente: mis reservas")).pack(pady=5)

    # Opciones exclusivas de administrador
    if usuario_tipo_actual == "administrador":
        tk.Label(contenedor, text="Opciones de administrador", font=("Arial", 10, "italic")).pack(pady=(15, 5))

        tk.Button(contenedor, text="Registrar sala", width=ANCHO_BOTON, height=ALTO_BOTON,
          command=lambda: ventana_registrar_sala(ventana)).pack(pady=5)

        tk.Button(contenedor, text="Editar sala", width=ANCHO_BOTON, height=ALTO_BOTON,
                  command=lambda: print("Pendiente: editar sala")).pack(pady=5)

    tk.Button(contenedor, text="Cerrar sesión", width=ANCHO_BOTON, height=ALTO_BOTON,
              command=ventana.destroy).pack(pady=(20, 0))

def ventana_salas():
    ventana = tk.Toplevel()  # <-- Abre una ventana secundaria sobre la principal
    ventana.title('Listado de salas')
    ventana.geometry(VENTANA_DIMENSIONES)

    titulo = tk.Label(ventana, text='Listado de salas', font=('Arial', 16, 'bold'))
    titulo.pack(pady=10)

    columnas = ('id', 'nombre', 'ubicacion', 'capacidad', 'estado')
    tabla = ttk.Treeview(ventana, columns=columnas, show='headings')

    # --- AQUÍ VAN LOS ENCABEZADOS Y ANCHOS ---
    tabla.heading('id', text='ID')
    tabla.heading('nombre', text='Nombre')
    tabla.heading('ubicacion', text='Ubicación')
    tabla.heading('capacidad', text='Capacidad')
    tabla.heading('estado', text='Estado')

    tabla.column('id', width=40)
    tabla.column('nombre', width=140)
    tabla.column('ubicacion', width=120)
    tabla.column('capacidad', width=80)
    tabla.column('estado', width=120)
    # ------------------------------------------

    tabla.pack(fill='both', expand=True, padx=15, pady=10)

    salas = Sala.buscar_todos()
    
    if len(salas) == 0:
        mostrar_ventana('info', 'No hay salas registradas', ventana)

    for sala in salas:
        tabla.insert('', 'end', values=(sala.obtener_id(), sala.obtener_nombre(),
        sala.obtener_ubicacion(), sala.obtener_capacidad(), sala.obtener_estado()))

# OPCIONES ADMIN
def ventana_registrar_sala(ventana):
    formulario = tk.Toplevel(ventana)
    formulario.title("Registrar sala")
    formulario.geometry("350x300")

    tk.Label(formulario, text="Nombre").pack(pady=(10, 0))
    entry_nombre = tk.Entry(formulario)
    entry_nombre.pack()

    tk.Label(formulario, text="Ubicación").pack(pady=(10, 0))
    entry_ubicacion = tk.Entry(formulario)
    entry_ubicacion.pack()

    tk.Label(formulario, text="Capacidad").pack(pady=(10, 0))
    entry_capacidad = tk.Entry(formulario)
    entry_capacidad.pack()

    estado_var = tk.StringVar(value="Disponible")
    tk.Label(formulario, text="Estado").pack(pady=(10, 0))
    tk.OptionMenu(formulario, estado_var, "Disponible", "En mantenimiento").pack()

    def guardar():
        nombre = entry_nombre.get().strip()
        ubicacion = entry_ubicacion.get().strip()
        capacidad_texto = entry_capacidad.get().strip()

        if not nombre or not ubicacion or not capacidad_texto:
            mostrar_ventana("error", "Todos los campos son obligatorios.", formulario)
            return

        try:
            capacidad = int(capacidad_texto)
        except ValueError:
            mostrar_ventana("error", "La capacidad debe ser un número.", formulario)
            return

        resultado = registrar_sala(usuario_actual, nombre, ubicacion, capacidad, estado_var.get())

        if resultado is not None:
            mostrar_ventana("info", "Sala registrada correctamente.", formulario)
            formulario.destroy()

    tk.Button(formulario, text="Guardar", command=guardar).pack(pady=20)



def main():
    ventana = tk.Tk()
    ventana.title("Sistema de Reserva de Salas")
    ventana.geometry(VENTANA_DIMENSIONES)
    ventana_login(ventana)
    ventana.mainloop()

if __name__ == '__main__':
    main()

