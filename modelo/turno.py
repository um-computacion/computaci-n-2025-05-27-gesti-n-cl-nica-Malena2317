
from datetime import datetime
from modelo.paciente import Paciente 
from modelo.medico import Medico 
import locale
locale.setlocale(locale.LC_TIME, 'C')    

class Turno:
    def __init__(self, el_paciente, el_medico, fecha_y_hora, la_especialidad):
        self.__paciente = None
        self.__medico = None
        self.__fecha_hora = None
        self.__especialidad = ""

        if not isinstance(el_paciente, Paciente):
            raise TypeError("¡Error! El 'paciente' debe ser un objeto de la clase Paciente.")
        self.__paciente = el_paciente # Si está todo bien, lo guardo.

        if not isinstance(el_medico, Medico):
            raise TypeError("¡Error! El 'médico' debe ser un objeto de la clase Medico.")
        self.__medico = el_medico # Lo asigno.

        if not isinstance(fecha_y_hora, datetime):
            raise TypeError("¡Atención! La 'fecha_hora' debe ser un objeto de tipo datetime.")
        self.__fecha_hora = fecha_y_hora # La guardo.

        if not isinstance(la_especialidad, str) or not la_especialidad.strip():
            raise ValueError("¡La especialidad del turno no puede estar vacía o no ser texto!")
        self.__especialidad = la_especialidad.strip() # Guardo la especialidad, limpio los espacios.


    # --- Métodos para obtener información (los "getters") ---

    def obtener_paciente(self):
        # Devuelve el objeto Paciente de este turno.
        return self.__paciente

    def obtener_medico(self):
        # Devuelve el objeto Medico de este turno.
        return self.__medico

    def obtener_fecha_hora(self):
        # Devuelve el objeto datetime con la fecha y hora del turno.
        return self.__fecha_hora
    
    def obtener_especialidad(self):
        # Día del turno (en inglés, lo convertimos a español)
        dia = self.__fecha_hora.strftime("%A").capitalize()

        # Verificamos si el médico atiende esa especialidad ese día
        if self.__medico.atiende_especialidad(self.__especialidad, dia):
            return self.__especialidad



    # --- Método de Representación (__str__) ---

    def __str__(self):
        # Esto es para que el turno se vea "bonito" cuando lo imprimo.
        fecha_hora_formateada = self.__fecha_hora.strftime("%Y-%m-%d %H:%M")
        return (f"--- Detalles del Turno ---\n"
                f"Paciente: {self.__paciente.obtener_nombre()} (DNI: {self.__paciente.obtener_dni()})\n"
                f"Médico: {self.__medico.obtener_nombre()} (Matrícula: {self.__medico.obtener_matricula()})\n"
                f"Especialidad: {self.__especialidad}\n"
                f"Fecha y Hora: {fecha_hora_formateada}\n"
                f"--------------------------")