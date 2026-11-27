import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from consulta_salas import *
import binascii
from datetime import datetime, date


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

def generar_hash_password(password):
    salt = os.urandom(16)

    hash_password = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return (
        binascii.hexlify(salt).decode()
        + ":"
        + binascii.hexlify(hash_password).decode()
    )   

def ver_reservas():

    ventana = tk.Toplevel()
    ventana.title("Reservas")
    ventana.geometry("800x500")

    tk.Label(
        ventana,
        text="Listado de Reservas",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    columnas = (
        "id",
        "usuario",
        "sala",
        "fecha",
        "horario"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings"
    )

    tabla.heading("id", text="ID")
    tabla.heading("usuario", text="Usuario")
    tabla.heading("sala", text="Sala")
    tabla.heading("fecha", text="Fecha")
    tabla.heading("horario", text="Horario")

    tabla.column("id", width=60)
    tabla.column("usuario", width=150)
    tabla.column("sala", width=180)
    tabla.column("fecha", width=120)
    tabla.column("horario", width=180)

    tabla.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    reservas = Reserva.buscar_todos()

    if len(reservas) == 0:

        mostrar_ventana(
            "info",
            "No existen reservas registradas.",
            ventana
        )

        return

    for reserva in reservas:

        tabla.insert(
            "",
            "end",
            values=(
                reserva.obtener_id(),
                reserva.obtener_usuario().obtener_nombre(),
                reserva.obtener_sala().obtener_nombre(),
                reserva.obtener_fecha(),
                (
                    f"{reserva.obtener_horario().obtener_hora_inicio()} - "
                    f"{reserva.obtener_horario().obtener_hora_fin()}"
                )
            )
        )

from datetime import datetime

def reservar_sala():

    ventana = tk.Toplevel()
    ventana.title("Reserva de Sala")
    ventana.geometry("500x350")

    tk.Label(
        ventana,
        text="Registro de Reserva",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Fecha
    tk.Label(
        ventana,
        text="Fecha (AAAA-MM-DD):"
    ).pack()

    fecha_entry = tk.Entry(
        ventana,
        width=20
    )

    fecha_entry.pack(pady=5)

    # Horario
    tk.Label(
        ventana,
        text="Horario:"
    ).pack()

    horarios = Horario.buscar_todos()

    horario_combo = ttk.Combobox(
        ventana,
        state="readonly",
        width=40
    )

    horario_combo["values"] = [
        f"{h.obtener_hora_inicio()} - {h.obtener_hora_fin()}"
        for h in horarios
    ]

    horario_combo.pack(pady=5)

    # Salas
    tk.Label(
        ventana,
        text="Sala disponible:"
    ).pack()

    sala_combo = ttk.Combobox(
        ventana,
        state="readonly",
        width=40
    )

    sala_combo.pack(pady=5)

    salas_disponibles = []

    def actualizar_salas(event=None):

        nonlocal salas_disponibles

        fecha = fecha_entry.get().strip()

        if horario_combo.current() == -1:
            return

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return

        horario = horarios[horario_combo.current()]

        salas_disponibles = Sala.buscar_disponibles(
            fecha,
            horario.obtener_id()
        )

        sala_combo["values"] = [
            f"{s.obtener_nombre()} (ID:{s.obtener_id()})"
            for s in salas_disponibles
        ]

        if len(salas_disponibles) > 0:
            sala_combo.current(0)
        else:
            sala_combo.set("")

    horario_combo.bind(
        "<<ComboboxSelected>>",
        actualizar_salas
    )

    fecha_entry.bind(
        "<KeyRelease>",
        actualizar_salas
    )

    def guardar_reserva():

        fecha = fecha_entry.get().strip()

        try:
            fecha_reserva = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            mostrar_ventana(
                "error",
                "La fecha debe tener formato AAAA-MM-DD.",
                ventana
            )
            return

        if fecha_reserva < date.today():

            mostrar_ventana(
                "error",
                "No es posible reservar una fecha anterior al día de hoy.",
                ventana
            )

            return
        if horario_combo.current() == -1:
            mostrar_ventana(
                "error",
                "Debe seleccionar un horario.",
                ventana
            )
            return

        if sala_combo.current() == -1:
            mostrar_ventana(
                "error",
                "Debe seleccionar una sala.",
                ventana
            )
            return

        try:

            horario = horarios[horario_combo.current()]
            sala = salas_disponibles[sala_combo.current()]

            reserva = Reserva(
                usuario_actual,
                sala,
                horario,
                fecha
            )

            reserva.guardar()

            mostrar_ventana(
                "info",
                "Reserva registrada correctamente.",
                ventana
            )

            ventana.destroy()

        except Exception as e:

            mostrar_ventana(
                "error",
                f"Error al guardar la reserva:\n{e}",
                ventana
            )

    tk.Button(
    ventana,
    text="Guardar Reserva",
    width=20,
    font=("Arial", 10, "bold"),
    command=guardar_reserva
).pack(pady=15)


def ventana_salas():
    ventana = tk.Tk()
    ventana.title('Listado de salas')
    ventana.geometry(VENTANA_DIMENSIONES)

    tk.Label(
        ventana,
        text=f"Bienvenido {usuario_actual.obtener_nombre()}",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    tk.Button(
        ventana,
        text="Reservar Sala",
        width=30,
        font=('Arial', 10),
        command=lambda: reservar_sala()
    ).pack(pady=8)

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

    if usuario_tipo_actual == "administrador":
        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=8)

        tk.Button(
        frame_botones,
        text="ver reservas",
        width=20,
        font=('Arial', 10),
        command=lambda: ver_reservas()
        ).pack(side='left', padx=5)

        tk.Button(
        frame_botones,
        text="Crear Usuario",
        width=20,
        font=('Arial', 10),
        command=lambda: ventana.destroy()
        ).pack(side='left', padx=5)

        tk.Button(
        frame_botones,
        text="Crear Sala",
        width=20,
        font=('Arial', 10),
        command=lambda: ventana.destroy()
        ).pack(side='left', padx=5)
    
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

