import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from consulta_salas import *

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

def ventana_salas():
    ventana = tk.Tk()
    ventana.title('Listado de salas')
    ventana.geometry(VENTANA_DIMENSIONES)

    titulo = tk.Label(ventana, text = 'Listado de salas', font = ('Arial', 16, 'bold'))
    titulo.pack(pady=10)

    columnas = ('id', 'nombre', 'ubicacion','capacidad','estado')
    tabla = ttk.Treeview(ventana, columns=columnas, show='headings')

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

    tabla.pack(fill='both', expand=True, padx=15, pady=10)

    salas = Sala.buscar_todos()
    
    if len(salas) == 0:
        mostrar_ventana('info', 'No hay salas registradas', ventana)

    for sala in salas:
        tabla.insert('', 'end', values=(sala.obtener_id(), sala.obtener_nombre(),
        sala.obtener_ubicacion(), sala.obtener_capacidad(), sala.obtener_estado()))
    
    ventana.mainloop()



def ventana_login():
    login = tk.Tk()
    login.title("Inicio de Sesión")
    login.geometry("350x200")

    tk.Label(login, text="Usuario").pack(pady=5)
    username_entry = tk.Entry(login)
    username_entry.pack()

    tk.Label(login, text="Contraseña").pack(pady=5)
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()

    def iniciar_sesion():
        global usuario_actual, usuario_tipo_actual
        username = username_entry.get().strip()
        password = password_entry.get()

        if not username or not password:
            mostrar_ventana("error", "Debe ingresar usuario y contraseña.", login)
            return

        try:
            usuario = Usuario.iniciar_sesion(username, password)
            if usuario is None:
                mostrar_ventana("error", "Usuario o contraseña incorrectos.", login)
                return

            usuario_actual = usuario
            if isinstance(usuario, Administrador):
                usuario_tipo_actual = "administrador"
            else:
                usuario_tipo_actual = "empleado"

            login.destroy()
            ventana_salas()
        except Exception as e:
            mostrar_ventana("error", f"Error al iniciar sesión:\n{e}", login)

    tk.Button(login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=15)
    login.mainloop()

if __name__ == '__main__':
    ventana_login()

