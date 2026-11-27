import os
import hashlib
from abc import ABC, abstractmethod
from conexion import Conexion, ActiveRecord


class Usuario(ABC):
    def __init__(self, id_usuario: int, username: str, nombre: str, apellido: str, telefono: str, email: str, password_hash: str):
        self.__id_usuario = id_usuario
        self.__username = username
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email
        self.__password_hash = password_hash

    def obtener_id(self):
        return self.__id_usuario

    def obtener_username(self):
        return self.__username

    def obtener_nombre(self):
        return self.__nombre

    def obtener_apellido(self):
        return self.__apellido

    def obtener_telefono(self):
        return self.__telefono

    def obtener_email(self):
        return self.__email

    def obtener_password_hash(self):
        return self.__password_hash

    @classmethod
    def crear_usuario(cls, username: str, nombre: str, apellido: str, telefono: str, email: str, password: str, tipo_usuario: str = 'empleado', confirmar: bool = True) -> int:
        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()
        password_hash = cls.generar_hash(password)
        sql = """
        INSERT INTO Usuario (username, nombre, apellido, telefono, email, password_hash, tipo_usuario)
        VALUES (%s, %s, %s, %s, %s, %s, %s) 
        """
        try:
            cursor.execute(
                sql, 
                (username, nombre, apellido, telefono, email, password_hash, tipo_usuario)
            )
            id_usuario = cursor.lastrowid
            if confirmar: 
                cnn.commit()
            return id_usuario
        except Exception:
            if confirmar:
                cnn.rollback()
            raise
        finally:
            cursor.close()
    
    @staticmethod
    def generar_hash(password: str) -> str:
        salt = os.urandom(32)
        hash_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt.hex() + ":" + hash_password.hex()

    @staticmethod
    def verificar_password(password, hash_guardado):
        if ":" in hash_guardado:
            salt_hex, hash_hex = hash_guardado.split(":", 1)
            salt = bytes.fromhex(salt_hex)
            hash_calculado = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                100000
            )
            return hash_calculado.hex() == hash_hex
        
        # Respaldo si en la BD está guardado como SHA-256 simple o texto plano
        sha256_simple = hashlib.sha256(password.encode()).hexdigest()
        return hash_guardado == sha256_simple or hash_guardado == password

    
    @classmethod
    def iniciar_sesion(cls, username: str, password: str):
        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()

        sql = """
        SELECT id_usuario, username, nombre, apellido, telefono, email, password_hash, tipo_usuario
        FROM Usuario
        WHERE username = %s
        """
        cursor.execute(sql, (username,))
        registro = cursor.fetchone()
        cursor.close()
        
        if registro is None:
            return None

        id_usuario, username, nombre, apellido, telefono, email, password_hash_db, tipo_usuario = registro

        if not cls.verificar_password(password, password_hash_db):
            return None
        
        if tipo_usuario.lower() == "administrador":
            return Administrador(id_usuario, username, nombre, apellido, telefono, email, password_hash_db)
        else:
            return Empleado(id_usuario, username, nombre, apellido, telefono, email, password_hash_db)

    @abstractmethod
    def mostrar(self):
        pass


class Administrador(Usuario):
    def mostrar(self):
        return f"Admin: {self.obtener_nombre()} {self.obtener_apellido()}"


class Empleado(Usuario):
    def mostrar(self):
        return f"Empleado: {self.obtener_nombre()} {self.obtener_apellido()}"


class Sala(ActiveRecord):
    def __init__(self, id_sala: int, nombre: str, ubicacion: str, capacidad: int, estado: str):
        self.__id_sala = id_sala
        self.__nombre = nombre
        self.__ubicacion = ubicacion
        self.__capacidad = capacidad
        self.__estado = estado

    def obtener_id(self):
        return self.__id_sala

    def obtener_nombre(self):
        return self.__nombre

    def obtener_ubicacion(self):
        return self.__ubicacion

    def obtener_capacidad(self):
        return self.__capacidad

    def obtener_estado(self):
        return self.__estado

    def guardar(self):
        pass

    def actualizar(self) -> None:
        pass

    def eliminar(self) -> None:
        pass

    @classmethod
    def buscar_disponibles(cls, fecha, id_horario):

        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()

        sql = """
        SELECT id_sala, nombre, ubicacion, capacidad, estado
        FROM Sala
        WHERE estado = 'Disponible'
        AND id_sala NOT IN (
            SELECT id_sala
            FROM Reserva
            WHERE fecha = %s
            AND id_horario = %s
        )
        ORDER BY nombre
        """

        cursor.execute(sql, (fecha, id_horario))
        filas = cursor.fetchall()
        cursor.close()

        return [cls(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    @classmethod
    def buscar_por_id(cls, id_sala: int):
        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()
        sql = "SELECT id_sala, nombre, ubicacion, capacidad, estado FROM Sala WHERE id_sala = %s"
        cursor.execute(sql, (id_sala,))
        fila = cursor.fetchone()
        cursor.close()
        if fila:
            return cls(fila[0], fila[1], fila[2], fila[3], fila[4])
        return None

    @classmethod
    def buscar_todos(cls):
        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()
        sql = "SELECT id_sala, nombre, ubicacion, capacidad, estado FROM Sala ORDER BY nombre"
        cursor.execute(sql)
        filas = cursor.fetchall()
        cursor.close()
        return [cls(f[0], f[1], f[2], f[3], f[4]) for f in filas]

class Horario:

    def __init__(self, id_horario, hora_inicio, hora_fin):
        self.__id_horario = id_horario
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin

    def obtener_id(self):
        return self.__id_horario

    def obtener_hora_inicio(self):
        return self.__hora_inicio

    def obtener_hora_fin(self):
        return self.__hora_fin

    @classmethod
    def buscar_todos(cls):

        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()

        sql = """
        SELECT id_horario, hora_inicio, hora_fin
        FROM Horario
        ORDER BY hora_inicio
        """

        cursor.execute(sql)

        filas = cursor.fetchall()

        cursor.close()

        return [
            cls(f[0], f[1], f[2])
            for f in filas
        ]


class Reserva(ActiveRecord):

    def __init__(
        self,
        usuario: Usuario,
        sala: Sala,
        horario: Horario,
        fecha: str,
        id_reserva=None
    ):
        self.__id_reserva = id_reserva
        self.__usuario = usuario
        self.__sala = sala
        self.__horario = horario
        self.__fecha = fecha

    def obtener_id(self):
        return self.__id_reserva

    def obtener_usuario(self):
        return self.__usuario

    def obtener_sala(self):
        return self.__sala

    def obtener_horario(self):
        return self.__horario

    def obtener_fecha(self):
        return self.__fecha

    @classmethod
    def buscar_todos(cls):

        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()

        sql = """
        SELECT
            r.id_reserva,
            r.fecha,

            u.id_usuario,
            u.username,
            u.nombre,
            u.apellido,
            u.telefono,
            u.email,
            u.password_hash,
            u.tipo_usuario,

            s.id_sala,
            s.nombre,
            s.ubicacion,
            s.capacidad,
            s.estado,

            h.id_horario,
            h.hora_inicio,
            h.hora_fin

        FROM Reserva r

        INNER JOIN Usuario u
            ON r.id_usuario = u.id_usuario

        INNER JOIN Sala s
            ON r.id_sala = s.id_sala

        INNER JOIN Horario h
            ON r.id_horario = h.id_horario

        ORDER BY r.fecha, h.hora_inicio
        """

        cursor.execute(sql)

        filas = cursor.fetchall()

        cursor.close()

        reservas = []

        for fila in filas:

            (
                id_reserva,
                fecha,

                id_usuario,
                username,
                nombre,
                apellido,
                telefono,
                email,
                password_hash,
                tipo_usuario,

                id_sala,
                nombre_sala,
                ubicacion,
                capacidad,
                estado,

                id_horario,
                hora_inicio,
                hora_fin

            ) = fila

            # Usuario
            if tipo_usuario.lower() == "administrador":
                usuario = Administrador(
                    id_usuario,
                    username,
                    nombre,
                    apellido,
                    telefono,
                    email,
                    password_hash
                )
            else:
                usuario = Empleado(
                    id_usuario,
                    username,
                    nombre,
                    apellido,
                    telefono,
                    email,
                    password_hash
                )

            # Sala
            sala = Sala(
                id_sala,
                nombre_sala,
                ubicacion,
                capacidad,
                estado
            )

            # Horario
            horario = Horario(
                id_horario,
                hora_inicio,
                hora_fin
            )

            # Reserva
            reserva = cls(
                usuario,
                sala,
                horario,
                fecha,
                id_reserva
            )

            reservas.append(reserva)

        return reservas

    def guardar(self):

        cnn = Conexion().obtener_conexion()
        cursor = cnn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO Reserva
                (id_usuario, id_sala, id_horario, fecha)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    self.__usuario.obtener_id(),
                    self.__sala.obtener_id(),
                    self.__horario.obtener_id(),
                    self.__fecha
                )
            )

            self.__id_reserva = cursor.lastrowid

            cnn.commit()

        except Exception:
            cnn.rollback()
            raise

        finally:
            cursor.close()

    def actualizar(self):
        pass

    def eliminar(self):
        pass

    @classmethod
    def buscar_por_id(cls, id_reserva):
        pass

