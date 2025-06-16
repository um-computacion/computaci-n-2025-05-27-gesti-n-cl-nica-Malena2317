
class DNIInvalidoError(Exception):
    "Error si el DNI no tiene 8 números."
    def __init__(self, mensaje="DNI inválido: debe tener 8 números."):
        super().__init__(mensaje)

class NombreInvalidoError(Exception):
    "Error si el nombre está vacío."
    def __init__(self, mensaje="El nombre no puede estar vacío."):
        super().__init__(mensaje)

class FechaNacimientoInvalidaError(Exception):
    "Error si la fecha de nacimiento es inválida."
    def __init__(self, mensaje="La fecha debe tener formato dd/mm/aaaa y ser válida."):
        super().__init__(mensaje)

# --- Excepciones NUEVAS para la clase Medico ---

class MatriculaInvalidaError(Exception):
    "Error si la matrícula del médico está vacía o solo con espacios."
    def __init__(self, mensaje="La matrícula no puede estar vacía o con solo espacios."):
        super().__init__(mensaje)

class EspecialidadVaciaError(Exception):
    "Error si se intenta crear un médico sin especialidades o si se quitan todas."
    def __init__(self, mensaje="Un médico debe tener al menos una especialidad."):
        super().__init__(mensaje)

class EspecialidadDuplicadaError(Exception):
    "Error si se intenta agregar una especialidad que el médico ya tiene."
    def __init__(self, mensaje="Esa especialidad ya la tiene este médico."):
        super().__init__(mensaje)

# --- Excepciones Específicas de Especialidad ---

class EspecialidadError(Exception): # Una base para errores de Especialidad
    "Clase base para errores específicos de especialidades."
    pass

class TipoEspecialidadInvalidoError(EspecialidadError): # Hereda de la base de Especialidad
    "Error si el tipo de especialidad está vacío."
    def __init__(self, mensaje="El tipo de especialidad no puede estar vacío."):
        super().__init__(mensaje)

class DiasAtencionInvalidosError(EspecialidadError): # Hereda de la base de Especialidad
    "Error si los días de atención no son válidos o están vacíos."
    def __init__(self, mensaje="Días de atención inválidos: deben ser una lista no vacía de días válidos (lunes a domingo)."):
        super().__init__(mensaje)

# --- Excepciones para la Clase Clinica ---

class PacienteExistenteError(Exception):
    "Error cuando se intenta agregar un paciente que ya está registrado."
    def __init__(self, mensaje="¡Ups! Este paciente ya existe en el sistema."):
        super().__init__(mensaje)

class PacienteNoExisteError(Exception):
    "Error cuando se busca un paciente que no está registrado."
    def __init__(self, mensaje="¡Vaya! El paciente que buscas no está en nuestros registros."):
        super().__init__(mensaje)

class MedicoExistenteError(Exception):
    "Error cuando se intenta agregar un médico que ya está registrado."
    def __init__(self, mensaje="¡Uy! Este médico ya está registrado con esa matrícula."):
        super().__init__(mensaje)

class MedicoNoExisteError(Exception):
    "Error cuando se busca un médico que no está registrado."
    def __init__(self, mensaje="¡Lo siento! El médico que buscas no está registrado."):
        super().__init__(mensaje)

class TurnoDuplicadoError(Exception):
    "Error cuando se intenta agendar un turno que ya existe para ese médico y fecha/hora."
    def __init__(self, mensaje="¡Ya hay un turno agendado para ese médico en esa fecha y hora!"):
        super().__init__(mensaje)

class MedicoNoAtiendeEspecialidadError(Exception):
    "Error cuando el médico no atiende la especialidad solicitada para un turno."
    def __init__(self, mensaje="El médico no atiende la especialidad que solicitaste."):
        super().__init__(mensaje)

class MedicoNoTrabajaEseDiaError(Exception):
    "Error cuando se intenta agendar un turno un día que el médico no trabaja."
    def __init__(self, mensaje="El médico no trabaja el día de la semana para el turno solicitado."):
        super().__init__(mensaje)

class RecetaInvalidaError(Exception): # Aunque la clase Receta ya valida, Clinica podría tener un control extra.
    "Error cuando los datos de una receta no son válidos (ej. lista de medicamentos vacía)."
    def __init__(self, mensaje="No se puede emitir la receta: los datos son inválidos."):
        super().__init__(mensaje)