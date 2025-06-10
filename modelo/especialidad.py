
from modelo.exception import (TipoEspecialidadInvalidoError,DiasAtencionInvalidosError)

class Especialidad:
    # Una lista con los días de la semana válidos para chequear
    DIAS_VALIDOS_PARA_ATENCION = ["lunes", "martes", "miércoles", "miercoles", "jueves", "viernes", "sábado", "sabado", "domingo"]

    def __init__(self, tipo, dias_atencion):
        # Defino mis atributos privados
        self.__tipo = ""
        self.__dias = []

        # Primero, valido el nombre (tipo) de la especialidad
        if not tipo or tipo.strip() == "":
            raise TipoEspecialidadInvalidoError("El nombre de la especialidad no puede estar vacío.")
        self.__tipo = tipo.strip().capitalize() # Lo guardo limpio y con la primera letra en mayúscula

        # Ahora los días de atención
        if not dias_atencion or len(dias_atencion) == 0:
            raise DiasAtencionInvalidosError("Una especialidad tiene que tener días de atención.")
        
        dias_limpios_y_validos = []
        for d in dias_atencion:
            dia_temp = d.strip().lower() # Lo limpio y lo pongo en minúscula
            if dia_temp not in self.DIAS_VALIDOS_PARA_ATENCION:
                raise DiasAtencionInvalidosError(f"El día '{d}' no es un día válido de la semana.")
            # Si el día ya lo tengo, no lo agrego de nuevo (evito duplicados en la lista)
            if dia_temp not in dias_limpios_y_validos:
                dias_limpios_y_validos.append(dia_temp)
        
        self.__dias = sorted(dias_limpios_y_validos) # Guardo los días ordenados por si acaso

    # Método para obtener el nombre de la especialidad
    def obtener_tipo(self): # Me pidieron obtener_especialidad() pero el tipo es el nombre
        return self.__tipo

    # Método para saber si atiende en un día específico
    def verificar_dia(self, dia_a_chequear):
        dia_normalizado = dia_a_chequear.strip().lower() # Limpio y pongo en minúscula para comparar
        
        if dia_normalizado in self.__dias: # Me fijo si el día está en mi lista de días
            return True
        else:
            return False

    # Para que se vea bonito cuando lo imprimo
    def __str__(self):
        # Tengo que armar la lista de días para el texto
        dias_formateados = []
        for dia in self.__dias:
            dias_formateados.append(dia.capitalize())

        # Uno los días con comas y los meto en el formato final
        texto_dias = ", ".join(dias_formateados)
        return f"{self.__tipo} (Días: {texto_dias})"

    # Esto es para que las especialidades se puedan comparar entre sí, por su nombre para que no tenga especialidades duplicadas.
    def __eq__(self, other):
        if not isinstance(other, Especialidad): # Si no es una Especialidad, no se pueden comparar
            return NotImplemented
        return self.__tipo.lower() == other.__tipo.lower() # Comparo por el tipo, ignorando mayúsculas/minúsculas

    # Esto también es para que funcione bien en listas o sets, si lo uso.
    def __hash__(self):
        return hash(self.__tipo.lower())