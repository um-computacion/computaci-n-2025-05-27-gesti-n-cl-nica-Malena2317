
import unittest
from modelo.especialidad import Especialidad
from modelo.exception import ( TipoEspecialidadInvalidoError,DiasAtencionInvalidosError)

class TestEspecialidad(unittest.TestCase):

    def setUp(self):
        # Datos de especialidades que voy a usar en varios tests
        self.tipo_valido = "Cardiología"
        self.dias_validos_1 = ["lunes", "miércoles", "viernes"]
        self.dias_validos_2 = ["Martes", "JUEVES"] # Con mayúsculas para probar
        self.dias_validos_cortos = ["lunes"] # Para probar con un solo día

    # --- Tests para cuando se crea una Especialidad (el constructor) ---

    def test_crear_especialidad_con_datos_correctos_funciona_bien(self):
        # Especialidad  de forma normal.
        esp = Especialidad(self.tipo_valido, self.dias_validos_1)
        
        # Me aseguro que no sea None y que los datos se guarden como espero
        self.assertIsNotNone(esp)
        self.assertEqual(esp.obtener_tipo(), "Cardiología")
        self.assertEqual(esp.obtener_dias_atencion(), ["lunes", "miércoles", "viernes"])
        self.assertEqual(len(esp.obtener_dias_atencion()), 3)

    def test_crear_especialidad_con_dias_validos_pero_en_distintas_mayusculas_los_guarda_en_minusculas(self):
        # La consigna dice que los días deben guardarse en minúsculas.
        esp = Especialidad("Neurología", self.dias_validos_2)
        self.assertEqual(esp.obtener_tipo(), "Neurología")
        self.assertEqual(esp.obtener_dias_atencion(), ["jueves", "martes"]) # Tienen que estar ordenados alfabéticamente también

    def test_crear_especialidad_con_dias_duplicados_en_la_lista_inicial_los_guarda_sin_duplicar(self):
        # Si le paso días repetidos al crear, solo debe guardar uno de cada.
        dias_con_duplicados = ["lunes", "lunes", "martes", "Martes"]
        esp = Especialidad("Dermatología", dias_con_duplicados)
        self.assertEqual(len(esp.obtener_dias_atencion()), 2)
        self.assertIn("lunes", esp.obtener_dias_atencion())
        self.assertIn("martes", esp.obtener_dias_atencion())

    # --- Tests para los errores al crear una Especialidad (validaciones) ---

    def test_crear_especialidad_con_nombre_vacio_lanza_error(self):
        # El nombre de la especialidad no puede ser un string vacío.
        with self.assertRaises(TipoEspecialidadInvalidoError):
            Especialidad("", self.dias_validos_1)
        
        with self.assertRaises(TipoEspecialidadInvalidoError):
            Especialidad("   ", self.dias_validos_1) # O solo espacios

    def test_crear_especialidad_sin_dias_de_atencion_lanza_error(self):
        # La lista de días no puede estar vacía.
        with self.assertRaises(DiasAtencionInvalidosError):
            Especialidad(self.tipo_valido, []) # Lista de días vacía
        
        with self.assertRaises(DiasAtencionInvalidosError):
            Especialidad(self.tipo_valido, None) # Si se pasa None, también debería fallar

    def test_crear_especialidad_con_dia_invalido_lanza_error(self):
        # Si pongo un día que no existe en la semana, debe dar error.
        dias_con_uno_malo = ["lunes", "día raro", "miércoles"]
        with self.assertRaises(DiasAtencionInvalidosError):
            Especialidad(self.tipo_valido, dias_con_uno_malo)
        
        dias_otro_malo = ["23/12/2024"] # Una fecha no es un día
        with self.assertRaises(DiasAtencionInvalidosError):
            Especialidad(self.tipo_valido, dias_otro_malo)

    # --- Tests para el método 'obtener_tipo()' (mi obtener_especialidad()) ---

    def test_obtener_tipo_devuelve_el_nombre_correcto(self):
        # Quiero ver si el método me devuelve el nombre de la especialidad bien.
        esp = Especialidad("Oftalmología", self.dias_validos_1)
        self.assertEqual(esp.obtener_tipo(), "Oftalmología")

    # --- Tests para el método 'verificar_dia()' ---

    def test_verificar_dia_devuelve_true_para_dias_que_si_atiende(self):
        # Pruebo con días que sí están en la lista de la especialidad.
        esp = Especialidad("Pediatría", ["lunes", "martes"])
        self.assertTrue(esp.verificar_dia("lunes"))
        self.assertTrue(esp.verificar_dia("MARTES")) # También con mayúsculas/minúsculas
        self.assertTrue(esp.verificar_dia("  lunes  ")) # Y con espacios

    def test_verificar_dia_devuelve_false_para_dias_que_no_atiende(self):
        # Pruebo con días que no están en la lista.
        esp = Especialidad("Pediatría", ["lunes", "martes"])
        self.assertFalse(esp.verificar_dia("miércoles"))
        self.assertFalse(esp.verificar_dia("Domingo"))
        self.assertFalse(esp.verificar_dia("   ")) # Un día vacío tampoco
        self.assertFalse(esp.verificar_dia("otro día"))

    # --- Test para el método '__str__()' (cómo se ve la especialidad) ---

    def test_str_especialidad_devuelve_formato_correcto(self):
        # Este test es para ver si la representación en texto es la que se me pidió.
        esp_para_str = Especialidad("Traumatología", ["lunes", "miércoles", "viernes"])
        expected_output = "Traumatología (Días: Lunes, Miércoles, Viernes)" 

        esp_un_dia = Especialidad("Odontología", ["jueves"])
        expected_output_un_dia = "Odontología (Días: Jueves)"
        self.assertEqual(str(esp_un_dia), expected_output_un_dia)

    # --- Tests para los métodos de comparación (__eq__ y __hash__) ---

    def test_especialidades_con_mismo_tipo_son_iguales_sin_importar_mayusculas(self):
        # Dos especialidades son iguales si tienen el mismo tipo, aunque una sea mayúscula y otra minúscula.
        esp1 = Especialidad("Cardiología", ["lunes"])
        esp2 = Especialidad("cardiología", ["martes"]) # Días distintos no importan para __eq__
        esp3 = Especialidad("CARDIOLOGÍA", ["miércoles"])
        esp_diferente = Especialidad("Pediatría", ["lunes"])

        self.assertEqual(esp1, esp2)
        self.assertEqual(esp1, esp3)
        self.assertNotEqual(esp1, esp_diferente)

    def test_especialidades_con_mismo_tipo_tienen_mismo_hash(self):
        # Para que funcionen bien en sets o diccionarios.
        esp1 = Especialidad("Radiología", ["lunes"])
        esp2 = Especialidad("radiología", ["martes"])
        esp_diferente = Especialidad("Cirugía", ["lunes"])

        self.assertEqual(hash(esp1), hash(esp2))
        self.assertNotEqual(hash(esp1), hash(esp_diferente))

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)