import unittest
from modelo.medico import Medico
from modelo.especialidad import Especialidad 
from modelo.exception import ( NombreInvalidoError,MatriculaInvalidaError,EspecialidadVaciaError,EspecialidadDuplicadaError,TypeError)

class TestMedico(unittest.TestCase):

    def setUp(self):
        self.pediatria = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.cardiologia = Especialidad("Cardiología", ["martes", "jueves"])
        self.dermatologia = Especialidad("Dermatología", ["viernes"])
        self.neurologia = Especialidad("Neurología", ["Martes", "Viernes"])

    # --- Pruebas para cuando creo un Médico (el constructor) ---

    def test_crear_medico_funciona_bien_con_una_especialidad(self):
        medico_basico = Medico("Dr. Marcos Garcíia", "MP45678", [self.pediatria])
        self.assertIsNotNone(medico_basico) 
        self.assertEqual(medico_basico.obtener_nombre(), "Dr. Marcos Garcíia")
        self.assertEqual(medico_basico.obtener_matricula(), "MP45678")
        self.assertEqual(len(medico_basico.obtener_especialidades()), 1)
        self.assertIn(self.pediatria, medico_basico.obtener_especialidades())

    def test_crear_medico_funciona_bien_con_varias_especialidades(self):
        medico_completo = Medico("Dra. Julieta Paz", "MP98765", [self.pediatria, self.cardiologia, self.dermatologia])
        self.assertEqual(len(medico_completo.obtener_especialidades()), 3)
        self.assertIn(self.pediatria, medico_completo.obtener_especialidades())
        self.assertIn(self.cardiologia, medico_completo.obtener_especialidades())
        self.assertIn(self.dermatologia, medico_completo.obtener_especialidades())

    # --- Pruebas para los errores en el constructor (validaciones) ---

    def test_crear_medico_con_nombre_vacio_o_blanco(self):
        with self.assertRaises(NombreInvalidoError):
            Medico("", "MP11111", [self.pediatria]) # Nombre vacío
        with self.assertRaises(NombreInvalidoError):
            Medico("   ", "MP22222", [self.cardiologia]) # Solo espacios

    def test_crear_medico_con_matricula_vacia_o_blanca(self):
        with self.assertRaises(MatriculaInvalidaError):
            Medico("Dr. Sin Matrícula", "", [self.pediatria]) # Matrícula vacía
        with self.assertRaises(MatriculaInvalidaError):
            Medico("Dra. Sin Matrícula 2", "  ", [self.dermatologia]) # Solo espacios

    def test_crear_medico_sin_especialidades_iniciales(self):
        with self.assertRaises(EspecialidadVaciaError):
            Medico("Dr. Nadie", "MP33333", []) # Lista de especialidades vacía
        with self.assertRaises(EspecialidadVaciaError):
            Medico("Dra. Nadie Mas", "MP44444", None) # O si la lista es None

    def test_crear_medico_con_especialidades_duplicadas_al_inicio(self):
        with self.assertRaises(EspecialidadDuplicadaError):
            Medico("Dr. Doble", "MP55555", [self.pediatria, self.pediatria]) # Pediatría dos veces
        pediatria_mayus = Especialidad("PEDIATRÍA", ["lunes"]) # Misma especialidad pero con mayúsculas/minúsculas 
        with self.assertRaises(EspecialidadDuplicadaError):
            Medico("Dra. Doble Mayus", "MP66666", [self.pediatria, pediatria_mayus])

    def test_crear_medico_con_algo_que_no_es_especialidad(self):
        with self.assertRaises(TypeError):
            Medico("Dr. Tipo Mal", "MP77777", [self.pediatria, "esto no es una especialidad"])
        with self.assertRaises(TypeError):
            Medico("Dra. Tipo Mal 2", "MP88888", [123, self.cardiologia])

    # --- Pruebas para el método 'agregar_especialidad' ---

    def test_agregar_especialidad_nueva_funciona(self):
        med = Medico("Dr. Agregador", "MP99999", [self.pediatria])
        cantidad_antes = len(med.obtener_especialidades())
        med.agregar_especialidad(self.dermatologia) # Le agrego dermatología
        self.assertEqual(len(med.obtener_especialidades()), cantidad_antes + 1) # Ahora tiene una más
        self.assertIn(self.dermatologia, med.obtener_especialidades()) # Y debe ser la que agregué

    def test_agregar_especialidad_existente(self):
        med = Medico("Dra. AntiDuplicados", "MP00001", [self.cardiologia])
        with self.assertRaises(EspecialidadDuplicadaError):
            med.agregar_especialidad(self.cardiologia) # Ya la tiene
        cardiologia_mayus = Especialidad("CARDIOLOGÍA", ["jueves"])  # Misma especialidad pero con mayúsculas/minúsculas 
        with self.assertRaises(EspecialidadDuplicadaError):
            med.agregar_especialidad(cardiologia_mayus)

    def test_agregar_algo_que_no_es_especialidad(self):
        med = Medico("Dr. NoEntiende", "MP00002", [self.pediatria])
        with self.assertRaises(TypeError):
            med.agregar_especialidad("cadena de texto") # No es un objeto Especialidad
        with self.assertRaises(TypeError):
            med.agregar_especialidad(999) # Un número tampoco

    # --- Pruebas para el método 'obtener_especialidad_para_dia' ---

    def test_obtener_especialidad_para_dia_que_atiende_devuelve_nombre_correcto(self):
        # Quiero saber si me devuelve la especialidad correcta para un día de atención.
        med = Medico("Dr. Buscador", "MP00003", [self.pediatria, self.dermatologia])
        
        self.assertEqual(med.obtener_especialidad_para_dia("lunes"), "Pediatría")
        self.assertEqual(med.obtener_especialidad_para_dia("VIERNES"), "Dermatología") # Prueba con mayúsculas
        self.assertEqual(med.obtener_especialidad_para_dia("  miércoles  "), "Pediatría") # Prueba con espacios

    def test_obtener_especialidad_para_dia_que_no_atiende_devuelve_none(self):
        # Si el médico no atiende ningún día, la función debe decirme que no hay nada.
        med = Medico("Dra. Libre", "MP00004", [self.cardiologia]) # Solo atiende martes y jueves
        
        self.assertIsNone(med.obtener_especialidad_para_dia("lunes"))
        self.assertIsNone(med.obtener_especialidad_para_dia("domingo"))
        self.assertIsNone(med.obtener_especialidad_para_dia("")) # Un día vacío tampoco sirve.

    # --- Prueba para el método '__str__' (cómo se ve el médico impreso) ---

    def test_str_formato_de_salida_es_el_esperado(self):
        med_para_str = Medico("Dra. Imprimible", "MP00005", [self.cardiologia, self.neurologia])
        expected_output = (
            "Dra. Imprimible,\n"
            "MP00005,\n"
            "[\n"
            "  Cardiología (Días: Martes, Jueves),\n" # Ordenadas como se pasan en la lista inicial
            "  Neurología (Días: Martes, Viernes)\n"
            "]"
        )
        self.assertEqual(str(med_para_str), expected_output)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)