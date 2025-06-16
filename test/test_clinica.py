import unittest
from datetime import datetime
from modelo.clinica import Clinica
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from modelo.exception import (
    PacienteExistenteError, PacienteNoExisteError,
    MedicoExistenteError, MedicoNoExisteError,
    TurnoDuplicadoError, MedicoNoAtiendeEspecialidadError,
    MedicoNoTrabajaEseDiaError
)

class TestClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.especialidad_pediatria = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.especialidad_cardiologia = Especialidad("Cardiología", ["martes", "jueves"])
        self.paciente = Paciente("Ana García", "12345678", "01/01/1990")
        self.medico = Medico("Dr. Juan Pérez", "MP11111", [self.especialidad_pediatria])
        self.medico2 = Medico("Dra. María López", "MP22222", [self.especialidad_cardiologia])
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        self.clinica.agregar_medico(self.medico2)

    def test_agregar_paciente_exitoso(self):
        nuevo = Paciente("Carlos Pérez", "87654321", "02/02/1980")
        self.clinica.agregar_paciente(nuevo)
        self.assertIn(nuevo, self.clinica.obtener_pacientes())

    def test_agregar_paciente_duplicado(self):
        with self.assertRaises(PacienteExistenteError):
            self.clinica.agregar_paciente(self.paciente)

    def test_agregar_medico_exitoso(self):
        nuevo = Medico("Dr. José Ruiz", "MP33333", [self.especialidad_pediatria])
        self.clinica.agregar_medico(nuevo)
        self.assertIn(nuevo, self.clinica.obtener_medicos())

    def test_agregar_medico_duplicado(self):
        with self.assertRaises(MedicoExistenteError):
            self.clinica.agregar_medico(self.medico)

    def test_agendar_turno_exitoso(self):
        fecha = datetime(2025, 6, 16, 10, 0)  # Lunes
        turno = self.clinica.agendar_turno("12345678", "MP11111", "Pediatría", fecha)
        self.assertEqual(turno.obtener_fecha_hora(), fecha)

    def test_agendar_turno_paciente_no_existe(self):
        fecha = datetime(2025, 6, 16, 10, 0)
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.agendar_turno("99999999", "MP11111", "Pediatría", fecha)

    def test_agendar_turno_medico_no_existe(self):
        fecha = datetime(2025, 6, 16, 10, 0)
        with self.assertRaises(MedicoNoExisteError):
            self.clinica.agendar_turno("12345678", "MP99999", "Pediatría", fecha)

    def test_agendar_turno_duplicado(self):
        fecha = datetime(2025, 6, 16, 10, 0)
        self.clinica.agendar_turno("12345678", "MP11111", "Pediatría", fecha)
        paciente2 = Paciente("Luis Díaz", "55555555", "03/03/1985")
        self.clinica.agregar_paciente(paciente2)
        with self.assertRaises(TurnoDuplicadoError):
            self.clinica.agendar_turno("55555555", "MP11111", "Pediatría", fecha)

    def test_agendar_turno_medico_no_atiende_especialidad(self):
        fecha = datetime(2025, 6, 17, 10, 0)  # Martes, día que sí trabaja Dra. María López
        with self.assertRaises(MedicoNoAtiendeEspecialidadError):
            self.clinica.agendar_turno("12345678", "MP22222", "Pediatría", fecha)


    def test_agendar_turno_medico_no_trabaja_dia(self):
        fecha = datetime(2025, 6, 18, 10, 0)  # Miércoles
        with self.assertRaises(MedicoNoTrabajaEseDiaError):
            self.clinica.agendar_turno("12345678", "MP22222", "Cardiología", fecha)

    def test_emitir_receta_exitoso(self):
        receta = self.clinica.emitir_receta("12345678", "MP11111", ["Ibuprofeno"])
        self.assertIn("Ibuprofeno", receta.obtener_medicamentos())

    def test_emitir_receta_paciente_no_existe(self):
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.emitir_receta("99999999", "MP11111", ["Ibuprofeno"])

    def test_emitir_receta_medico_no_existe(self):
        with self.assertRaises(MedicoNoExisteError):
            self.clinica.emitir_receta("12345678", "MP99999", ["Ibuprofeno"])

    def test_obtener_historia_clinica_por_dni(self):
        historia = self.clinica.obtener_historia_clinica_por_dni("12345678")
        self.assertEqual(historia.obtener_paciente().obtener_dni(), "12345678")

    def test_obtener_historia_clinica_paciente_no_existe(self):
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.obtener_historia_clinica_por_dni("99999999")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
