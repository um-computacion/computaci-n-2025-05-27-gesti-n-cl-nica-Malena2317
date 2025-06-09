
class DNIInvalidoError(Exception):
    """Error si el DNI no tiene 8 números."""
    def __init__(self, mensaje="DNI inválido: debe tener 8 números."):
        super().__init__(mensaje)

class NombreInvalidoError(Exception):
    """Error si el nombre está vacío."""
    def __init__(self, mensaje="El nombre no puede estar vacío."):
        super().__init__(mensaje)

class FechaNacimientoInvalidaError(Exception):
    """Error si la fecha de nacimiento es inválida."""
    def __init__(self, mensaje="La fecha debe tener formato dd/mm/aaaa y ser válida."):
        super().__init__(mensaje)

# --- Excepciones NUEVAS para la clase Medico ---

class MatriculaInvalidaError(Exception):
    """Error si la matrícula del médico está vacía o solo con espacios."""
    def __init__(self, mensaje="La matrícula no puede estar vacía o con solo espacios."):
        super().__init__(mensaje)

class EspecialidadVaciaError(Exception):
    """Error si se intenta crear un médico sin especialidades o si se quitan todas."""
    def __init__(self, mensaje="Un médico debe tener al menos una especialidad."):
        super().__init__(mensaje)

class EspecialidadDuplicadaError(Exception):
    """Error si se intenta agregar una especialidad que el médico ya tiene."""
    def __init__(self, mensaje="Esa especialidad ya la tiene este médico."):
        super().__init__(mensaje)

# --- Excepciones Específicas de Especialidad ---
class EspecialidadError(Exception): # Una base para errores de Especialidad
    """Clase base para errores específicos de especialidades."""
    pass

class TipoEspecialidadInvalidoError(EspecialidadError): # Hereda de la base de Especialidad
    """Error si el tipo de especialidad está vacío."""
    def __init__(self, mensaje="El tipo de especialidad no puede estar vacío."):
        super().__init__(mensaje)

class DiasAtencionInvalidosError(EspecialidadError): # Hereda de la base de Especialidad
    """Error si los días de atención no son válidos o están vacíos."""
    def __init__(self, mensaje="Días de atención inválidos: deben ser una lista no vacía de días válidos (lunes a domingo)."):
        super().__init__(mensaje)