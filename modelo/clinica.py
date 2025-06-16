
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.turno import Turno
from modelo.receta import Receta
from modelo.historia_clinica import HistoriaClinica
from datetime import datetime
import locale 
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except locale.Error:
        print("Advertencia: No se pudo configurar el locale para español. Los días de la semana podrían salir en inglés.")

from modelo.exception import (PacienteExistenteError, PacienteNoExisteError,MedicoExistenteError, MedicoNoExisteError,TurnoDuplicadoError, MedicoNoAtiendeEspecialidadError,MedicoNoTrabajaEseDiaError,EspecialidadVaciaError)
class Clinica:
    def __init__(self):

        self.__pacientes: dict[str, Paciente] = {}      
        self.__medicos: dict[str, Medico] = {}          
        self.__historias_clinicas: dict[str, HistoriaClinica] = {} 
        self.__turnos: list[Turno] = [] 

    # --- Métodos para AGREGAR o REGISTRAR cosas ---

    def agregar_paciente(self, paciente: Paciente):

        if not isinstance(paciente, Paciente):
            raise TypeError("¡Error! Solo puedo agregar objetos de tipo Paciente.")
        
        if self.validar_existencia_paciente(paciente.obtener_dni()):
            raise PacienteExistenteError(f"¡Atención! El paciente con DNI {paciente.obtener_dni()} ya está registrado.")
        
        self.__pacientes[paciente.obtener_dni()] = paciente
        nueva_historia = HistoriaClinica(paciente)
        self.__historias_clinicas[paciente.obtener_dni()] = nueva_historia
        print(f"Paciente {paciente.obtener_nombre()} (DNI: {paciente.obtener_dni()}) registrado y su historia clínica creada.")

    def agregar_medico(self, medico: Medico):

        if not isinstance(medico, Medico):
            raise TypeError("¡Error! Solo puedo agregar objetos de tipo Medico.")
        if self.validar_existencia_medico(medico.obtener_matricula()):
            raise MedicoExistenteError(f"¡Atención! El médico con matrícula {medico.obtener_matricula()} ya está registrado.")
        
        # Si pasa las validaciones, lo agrego a mi lista de médicos.
        self.__medicos[medico.obtener_matricula()] = medico
        print(f"Médico {medico.obtener_nombre()} (Matrícula: {medico.obtener_matricula()}) registrado.")

    def agendar_turno(self, dni: str, matricula: str, especialidad_solicitada: str, fecha_hora: datetime):

        if not isinstance(especialidad_solicitada, str) or not especialidad_solicitada.strip():
            raise ValueError("¡Error! La especialidad solicitada para el turno no puede estar vacía.")
        
        if not self.validar_existencia_paciente(dni):
            raise PacienteNoExisteError(f"¡No puedo agendar! El paciente con DNI {dni} no está registrado.")
        
        if not self.validar_existencia_medico(matricula):
            raise MedicoNoExisteError(f"¡No puedo agendar! El médico con matrícula {matricula} no está registrado.")
    
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]

        if not isinstance(fecha_hora, datetime):
            raise TypeError("¡Error! La 'fecha_hora' debe ser un objeto datetime válido para agendar el turno.")
        
        if self.validar_turno_no_duplicado(matricula, fecha_hora):
            raise TurnoDuplicadoError(f"¡Imposible agendar! El médico {medico.obtener_nombre()} ya tiene un turno agendado para el {fecha_hora.strftime('%Y-%m-%d %H:%M')}.")

        dia_semana_espanol = self.obtener_dia_semana_en_espanol(fecha_hora)
        especialidad_que_atiende_ese_dia = medico.obtener_especialidad_para_dia(dia_semana_espanol)

        if especialidad_que_atiende_ese_dia is None:
            raise MedicoNoTrabajaEseDiaError(f"¡No se puede agendar! El médico {medico.obtener_nombre()} no atiende los días {dia_semana_espanol}.")
        
        if not self.validar_especialidad_en_dia(medico, especialidad_solicitada, dia_semana_espanol):
             raise MedicoNoAtiendeEspecialidadError(f"¡No se puede agendar! El médico {medico.obtener_nombre()} no atiende {especialidad_solicitada} los días {dia_semana_espanol}.")

        nuevo_turno = Turno(paciente, medico, fecha_hora, especialidad_solicitada.strip())
        self.__turnos.append(nuevo_turno)
        historia_paciente = self.__historias_clinicas[dni]
        historia_paciente.agregar_turno(nuevo_turno)
        print(f"Turno agendado con éxito: Paciente {paciente.obtener_nombre()} con Dr./Dra. {medico.obtener_nombre()} ({especialidad_solicitada}) el {fecha_hora.strftime('%Y-%m-%d %H:%M')}.")
        return nuevo_turno # Devuelvo el turno creado, por si lo necesitan.

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
      
        if not self.validar_existencia_paciente(dni):
            raise PacienteNoExisteError(f"¡No puedo emitir receta! El paciente con DNI {dni} no está registrado.")
        
        if not self.validar_existencia_medico(matricula):
            raise MedicoNoExisteError(f"¡No puedo emitir receta! El médico con matrícula {matricula} no está registrado.")
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]

        if not isinstance(medicamentos, list) or not all(isinstance(m, str) and m.strip() for m in medicamentos):
             raise ValueError("¡Error! La lista de medicamentos debe contener nombres válidos (texto no vacío).")
        if not medicamentos:
            raise ValueError("¡Error! La lista de medicamentos no puede estar vacía para una receta.")

        nueva_receta = Receta(paciente, medico, medicamentos)
        historia_paciente = self.__historias_clinicas[dni]
        historia_paciente.agregar_receta(nueva_receta)
        print(f"Receta emitida para Paciente: {paciente.obtener_nombre()} por Dr./Dra. {medico.obtener_nombre()}.")
        return nueva_receta # Devuelvo la receta creada.


    # --- Métodos para OBTENER información  ---

    def obtener_pacientes(self) -> list[Paciente]:
        return list(self.__pacientes.values()) 

    def obtener_medicos(self) -> list[Medico]:
        return list(self.__medicos.values()) 

    def obtener_medico_por_matricula(self, matricula: str) -> Medico:
        if not self.validar_existencia_medico(matricula):
            raise MedicoNoExisteError(f"Médico con matrícula {matricula} no encontrado.")
        return self.__medicos[matricula]

    def obtener_turnos(self) -> list[Turno]:
        return self.__turnos[:]

    def obtener_historia_clinica_por_dni(self, dni: str) -> HistoriaClinica:
        if not self.validar_existencia_paciente(dni):
            raise PacienteNoExisteError(f"No se encontró historia clínica para el DNI {dni}.")
        return self.__historias_clinicas[dni]


    # --- Métodos de VALIDACIÓN y UTILIDADES ---

    def validar_existencia_paciente(self, dni: str) -> bool:
        return dni in self.__pacientes

    def validar_existencia_medico(self, matricula: str) -> bool:
        return matricula in self.__medicos

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime) -> bool:

        for turno_existente in self.__turnos:

            if (turno_existente.obtener_medico().obtener_matricula() == matricula and
                turno_existente.obtener_fecha_hora() == fecha_hora):
                return True 
        return False 

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        return fecha_hora.strftime("%A").capitalize() # %A me da el nombre completo del día.

    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str) -> bool:
        especialidad_que_atiende = medico.obtener_especialidad_para_dia(dia_semana.lower()) 

        if especialidad_que_atiende is None:
            return False
        
        return especialidad_que_atiende.lower() == especialidad_solicitada.lower()


    # --- Método de Representación ---

    def __str__(self):

        pacientes_str = "\n".join([f"  - {p.obtener_nombre()} (DNI: {p.obtener_dni()})" for p in self.obtener_pacientes()])
        if not pacientes_str: pacientes_str = "  (No hay pacientes registrados)"

        # Resumen de médicos.
        medicos_str = "\n".join([f"  - {m.obtener_nombre()} (Matrícula: {m.obtener_matricula()})" for m in self.obtener_medicos()])
        if not medicos_str: medicos_str = "  (No hay médicos registrados)"

        # Resumen de turnos.

        total_turnos = len(self.__turnos)
        turnos_str = f"  Total de Turnos Agendados: {total_turnos}"

        # Resumen de historias clínicas (solo cuántas hay).
        total_historias = len(self.__historias_clinicas)
        historias_str = f"  Total de Historias Clínicas: {total_historias}"

        return (f"=== Resumen de la Clínica ===\n"
                f"Pacientes Registrados:\n{pacientes_str}\n"
                f"Médicos Registrados:\n{medicos_str}\n"
                f"Estadísticas:\n"
                f"{turnos_str}\n"
                f"{historias_str}\n"
                f"============================")