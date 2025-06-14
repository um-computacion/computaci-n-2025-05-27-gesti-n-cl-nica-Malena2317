from modelo.especialidad import Especialidad
from modelo.exception import (NombreInvalidoError,MatriculaInvalidaError,EspecialidadVaciaError,EspecialidadDuplicadaError)

class Medico:
    def __init__(self, nombre, matricula, especialidades):
        self.__nombre = "" 
        self.__matricula = ""
        self.__especialidades = []

        # Empiezo con las validaciones del nombre y la matrícula
        if not nombre or nombre.strip() == "": # Chequeo si está vacío o solo espacios
            raise NombreInvalidoError("El nombre del médico no puede estar vacío.")
        self.__nombre = nombre.strip() # Guardo el nombre sin espacios

        if not matricula or matricula.strip() == "":
            raise MatriculaInvalidaError("La matrícula del médico no puede estar vacía.")
        self.__matricula = matricula.strip()

        # Valido las especialidades 
        if not especialidades: # Si la lista está vacía
            raise EspecialidadVaciaError("Un médico debe tener al menos una especialidad al registrarse.")

        # Recorro las especialidades y las agrego esto me ayuda validar si hay duplicados o si no son objetos Especialidad.
        for esp in especialidades:
            if not isinstance(esp, Especialidad):
                raise TypeError("Cada elemento de la lista de especialidades debe ser un objeto Especialidad.")
            # La validación de 'in' en la lista ya usa el __eq__ de Especialidad.
            if esp in self.__especialidades:
                raise EspecialidadDuplicadaError(f"Especialidad '{esp.obtener_tipo()}' duplicada en la lista inicial.")
            self.__especialidades.append(esp)


    # Métodos para ver la informacion
    def obtener_nombre(self):
        return self.__nombre

    def obtener_matricula(self):
        return self.__matricula

    def obtener_especialidades(self):

        return self.__especialidades[:]

    # Método para agregar más especialidades
    def agregar_especialidad(self, nueva_especialidad):
        # Valido que sea una Especialidad
        if not isinstance(nueva_especialidad, Especialidad):
            raise TypeError("Solo se pueden agregar objetos de tipo Especialidad.")

        # Reviso si ya tiene esa especialidad para no agregarla otra vez
        if nueva_especialidad in self.__especialidades:
            raise EspecialidadDuplicadaError(f"El médico ya tiene la especialidad '{nueva_especialidad.obtener_tipo()}'.")
        
        self.__especialidades.append(nueva_especialidad) # La agrego si no está

    def obtener_especialidad_para_dia(self, dia):
        # Busco si el médico atiende alguna especialidad un día específico
        dia_buscado = dia.strip().lower() # Pongo el día en minúsculas para buscar mejor

        for esp in self.__especialidades:
            # Uso el método de Especialidad para ver sus días, que es lo correcto
            if dia_buscado in esp.obtener_dias_atencion():
                return esp.obtener_tipo() # Devuelvo el nombre de la especialidad
        return None # Si no encontré nada, devuelvo None

    # Cómo se ve mi objeto cuando lo imprimo
    def __str__(self):
        # Tengo que armar la lista de especialidades
        lista_info_especialidades = []
        for esp in self.__especialidades:
            lista_info_especialidades.append(str(esp)) # str(esp) va a usar el __str__ de Especialidad

        # Armo el texto de las especialidades, una por línea
        especialidades_formateadas = ",\n".join([f"  {info}" for info in lista_info_especialidades])

        # Este es el formato final que quiero que tenga
        return (f"{self.__nombre},\n"
                f"{self.__matricula},\n"
                f"[\n{especialidades_formateadas}\n]")