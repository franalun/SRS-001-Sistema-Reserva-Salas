use sistema_salas;

-- inserto usuario

insert into Usuario(username, nombre, apellido, telefono, email, password_hash)
values ('Admin01', 'matias', 'riquelme', '+56912345678', 'admin@mail.com', SHA2('123', 256));

-- inserto salas

insert into Sala(nombre, ubicacion, capacidad, estado)
values ('Sala de estudios 1', '4to piso', 15, 'Disponible');

-- inserto reservas

insert into Reserva(id_usuario, id_sala, fecha, hora)
values (1,1, curdate(), '14:30:00');