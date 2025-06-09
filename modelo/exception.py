
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