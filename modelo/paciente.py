from datetime import datetime
import re

from modelo.exception import DNIInvalidoError, NombreInvalidoError, FechaNacimientoInvalidaError

class Paciente:
    def __init__(self, nombre, dni, fecha_nacimiento):
        # Validación del nombre
        if nombre.strip() == "":
            raise NombreInvalidoError("El nombre no puede estar vacío")

        # Validación del DNI (8 números)
        if not re.match(r"^\d{8}$", dni): # O usar re.fullmatch(r"\d{8}", dni)
            raise DNIInvalidoError("DNI inválido. Debe tener 8 números")

        # Validación de la fecha
        try:
            fecha_obj = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
            if fecha_obj > datetime.now():
                raise FechaNacimientoInvalidaError("La fecha no puede ser futura")
        except ValueError:
            raise FechaNacimientoInvalidaError("Formato incorrecto. Usar dd/mm/aaaa")

        # Asignar atributos como privados
        self.__nombre = nombre
        self.__dni = dni
        self.__fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self):
        return self.__dni
    
    def obtener_nombre(self):
        return self.__nombre

    def __str__(self):
        # Acceder a los atributos privados
        return f"{self.__nombre}, {self.__dni}, {self.__fecha_nacimiento}"