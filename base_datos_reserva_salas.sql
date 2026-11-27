DROP DATABASE IF EXISTS sistema_salas;

CREATE DATABASE sistema_salas
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE sistema_salas;

CREATE TABLE Usuario(
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'empleado'
);

CREATE TABLE Sala(
    id_sala INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL,
    estado ENUM('Disponible', 'En mantenimiento') NOT NULL,

    CONSTRAINT chk_sala_capacidad
    CHECK(capacidad > 0)
);

CREATE TABLE Horario(
    id_horario INT PRIMARY KEY AUTO_INCREMENT,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

CREATE TABLE Reserva(
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_sala INT NOT NULL,
    id_horario INT NOT NULL,
    fecha DATE NOT NULL,

    CONSTRAINT fk_reserva_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES Usuario(id_usuario),

    CONSTRAINT fk_reserva_sala
        FOREIGN KEY (id_sala)
        REFERENCES Sala(id_sala),

    CONSTRAINT fk_reserva_horario
        FOREIGN KEY (id_horario)
        REFERENCES Horario(id_horario)
);

ALTER TABLE Reserva
ADD CONSTRAINT uq_reserva
UNIQUE(id_sala, id_horario, fecha);
