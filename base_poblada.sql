use sistema_salas;

-- inserto usuario

insert into Usuario(username, nombre, apellido, telefono, email, password_hash, tipo_usuario)
values ('Admin01', 'Matías', 'riquelme', '+56912345678', 'admin@mail.com', SHA2('123',256), 'Administrador');

insert into Usuario(username, nombre, apellido, telefono, email, password_hash)
values ('user01', 'Victor', 'Bustos', '+56967676767', 'user01@mail.com', SHA2('555',256));

-- inserto salas

insert into Sala(nombre, ubicacion, capacidad, estado)
values ('Sala de estudios 1', '4to piso', 15, 'Disponible');
insert into Sala(nombre, ubicacion, capacidad, estado)
values ('Sala de estudios 2', '4to piso', 10, 'Disponible');
insert into Sala(nombre, ubicacion, capacidad, estado)
values ('Sala de estudios 3', '4to piso', 15, 'En mantenimiento');

-- inserto horarios

INSERT INTO Horario (hora_inicio, hora_fin) VALUES
('08:00:00', '09:00:00'),
('09:00:00', '10:00:00'),
('10:00:00', '11:00:00'),
('11:00:00', '12:00:00'),
('12:00:00', '13:00:00'),
('14:00:00', '15:00:00'),
('15:00:00', '16:00:00'),
('16:00:00', '17:00:00'),
('17:00:00', '18:00:00');

-- inserto reservas

insert into Reserva(id_usuario, id_sala, id_horario, fecha)
values (1,1, 1, curdate());
