
from modelo.clinica import Clinica
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from modelo.turno import Turno
from modelo.receta import Receta
from modelo.historia_clinica import HistoriaClinica
from datetime import datetime, timedelta
import os
import locale

# Configuración del locale (se recomienda que esté en main.py o un archivo de configuración).
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except locale.Error:
        pass # Ignorar si no se puede configurar, los días saldrán en inglés.


# Excepciones personalizadas
from modelo.exception import (
    DNIInvalidoError, NombreInvalidoError, FechaNacimientoInvalidaError,
    MatriculaInvalidaError, EspecialidadVaciaError, EspecialidadDuplicadaError,
    TipoEspecialidadInvalidoError, DiasAtencionInvalidosError,
    PacienteExistenteError, PacienteNoExisteError,
    MedicoExistenteError, MedicoNoExisteError,
    TurnoDuplicadoError, MedicoNoAtiendeEspecialidadError,
    MedicoNoTrabajaEseDiaError, RecetaInvalidaError
)

class CLI:
    def __init__(self):
        self.__clinica = Clinica()

    def _limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _pausar_pantalla(self):
        input("\nPresiona Enter para continuar...")

    def _mostrar_menu(self):
        self._limpiar_pantalla()
        print("--- Menú Clínica ---")
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a médico")
        print("5) Emitir receta")
        print("6) Ver historia clínica de paciente")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")
        print("--------------------")

    def _solicitar_fecha_hora(self, mensaje):
        while True:
            fecha_str = input(f"{mensaje} (YYYY-MM-DD HH:MM): ")
            try:
                fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                if fecha_hora < datetime.now() - timedelta(minutes=1):
                    print("¡Error! La fecha y hora no pueden ser en el pasado.")
                    continue
                return fecha_hora
            except ValueError:
                print("¡Formato de fecha/hora incorrecto! Usa YYYY-MM-DD HH:MM (ej. 2025-12-31 14:30).")

    # --- Operaciones de Gestión ---

    def _agregar_paciente(self):
        self._limpiar_pantalla()
        print("--- Agregar Paciente ---")
        try:
            nombre = input("Nombre completo del paciente: ").strip()
            dni = input("DNI del paciente (8 números): ").strip()
            fecha_nac_str = input("Fecha de nacimiento (DD/MM/YYYY): ").strip()

            if not dni.isdigit() or len(dni) != 8:
                raise DNIInvalidoError("El DNI debe tener exactamente 8 números.")
            
            nuevo_paciente = Paciente(nombre, dni, fecha_nac_str)
            self.__clinica.agregar_paciente(nuevo_paciente)
            print("\n✅ Paciente agregado con éxito y su historia clínica creada.")
        except (DNIInvalidoError, NombreInvalidoError, FechaNacimientoInvalidaError, PacienteExistenteError, ValueError, TypeError) as e:
            print(f"\n❌ Error al agregar paciente: {e}")
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")
        self._pausar_pantalla()

    def _agregar_medico(self):
        self._limpiar_pantalla()
        print("--- Agregar Médico ---")
        try:
            nombre = input("Nombre completo del médico: ").strip()
            matricula = input("Matrícula del médico: ").strip()

            especialidades_lista = []
            print("\nIngresa las especialidades y días de atención ('fin' para terminar).")
            while True:
                tipo_especialidad = input("Tipo de especialidad: ").strip()
                if tipo_especialidad.lower() == 'fin': break
                
                dias_atencion_str = input("Días de atención (coma, ej. lunes, miércoles): ").strip().lower()
                dias_atencion = [d.strip() for d in dias_atencion_str.split(',') if d.strip()]
                
                try:
                    nueva_especialidad = Especialidad(tipo_especialidad, dias_atencion)
                    especialidades_lista.append(nueva_especialidad)
                    print(f"✅ Especialidad '{tipo_especialidad}' agregada provisionalmente.")
                except (TipoEspecialidadInvalidoError, DiasAtencionInvalidosError) as e:
                    print(f"❌ Error en la especialidad: {e}")
            
            if not especialidades_lista:
                raise EspecialidadVaciaError("Un médico debe tener al menos una especialidad.")

            nuevo_medico = Medico(nombre, matricula, especialidades_lista)
            self.__clinica.agregar_medico(nuevo_medico)
            print("\n✅ Médico agregado con éxito.")
        except (NombreInvalidoError, MatriculaInvalidaError, MedicoExistenteError, EspecialidadVaciaError, TypeError) as e:
            print(f"\n❌ Error al agregar médico: {e}")
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")
        self._pausar_pantalla()

    def _agendar_turno(self):
        self._limpiar_pantalla()
        print("--- Agendar Turno ---")
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matrícula del médico: ").strip()
            especialidad = input("Especialidad del turno: ").strip()
            fecha_hora = self._solicitar_fecha_hora("Fecha y hora del turno")

            self.__clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print("\n✅ Turno agendado exitosamente.")
        except (PacienteNoExisteError, MedicoNoExisteError, TurnoDuplicadoError, 
                MedicoNoAtiendeEspecialidadError, MedicoNoTrabajaEseDiaError, ValueError, TypeError) as e:
            print(f"\n❌ Error al agendar turno: {e}")
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")
        self._pausar_pantalla()

    def _agregar_especialidad_a_medico(self):
        self._limpiar_pantalla()
        print("--- Agregar Especialidad a Médico ---")
        try:
            matricula = input("Matrícula del médico: ").strip()
            medico = self.__clinica.obtener_medico_por_matricula(matricula) # Obtener médico para validar existencia.
            
            tipo_especialidad = input("Nuevo tipo de especialidad: ").strip()
            dias_atencion_str = input("Días de atención (coma, ej. lunes, miércoles): ").strip().lower()
            dias_atencion = [d.strip() for d in dias_atencion_str.split(',') if d.strip()]

            nueva_especialidad = Especialidad(tipo_especialidad, dias_atencion)
            medico.agregar_especialidad(nueva_especialidad)
            
            print("\n✅ Especialidad agregada con éxito al médico.")
        except (MedicoNoExisteError, TipoEspecialidadInvalidoError, DiasAtencionInvalidosError, EspecialidadDuplicadaError) as e:
            print(f"\n❌ Error al agregar especialidad: {e}")
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")
        self._pausar_pantalla()

    def _emitir_receta(self):
        self._limpiar_pantalla()
        print("--- Emitir Receta ---")
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matrícula del médico emisor: ").strip()
            
            medicamentos_lista = []
            print("\nIngresa los medicamentos ('fin' para terminar).")
            while True:
                medicamento = input(f"Medicamento {len(medicamentos_lista) + 1}: ").strip()
                if medicamento.lower() == 'fin': break
                if medicamento: medicamentos_lista.append(medicamento)
            
            if not medicamentos_lista:
                raise ValueError("Una receta debe tener al menos un medicamento.")

            self.__clinica.emitir_receta(dni, matricula, medicamentos_lista)
            print("\n✅ Receta emitida exitosamente.")
        except (PacienteNoExisteError, MedicoNoExisteError, ValueError, RecetaInvalidaError) as e:
            print(f"\n❌ Error al emitir receta: {e}")
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")
        self._pausar_pantalla()

    # --- Operaciones de Visualización ---

    def _ver_historia_clinica(self):
        self._limpiar_pantalla()
        print("--- Ver Historia Clínica ---")
        try:
            dni = input("DNI del paciente: ").strip()
            historia_clinica = self.__clinica.obtener_historia_clinica_por_dni(dni)
            print("\n" + str(historia_clinica))
        except PacienteNoExisteError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")
        self._pausar_pantalla()

    def _ver_todos_los_turnos(self):
        self._limpiar_pantalla()
        print("--- Todos los Turnos Agendados ---")
        turnos = self.__clinica.obtener_turnos()
        if not turnos:
            print("No hay turnos registrados en el sistema.")
        else:
            for i, turno in enumerate(turnos):
                print(f"\n--- Turno {i+1} ---")
                print(turno)
        self._pausar_pantalla()

    def _ver_todos_los_pacientes(self):
        self._limpiar_pantalla()
        print("--- Todos los Pacientes Registrados ---")
        pacientes = self.__clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados en el sistema.")
        else:
            for i, paciente in enumerate(pacientes):
                print(f"\n--- Paciente {i+1} ---")
                print(paciente)
        self._pausar_pantalla()

    def _ver_todos_los_medicos(self):
        self._limpiar_pantalla()
        print("--- Todos los Médicos Registrados ---")
        medicos = self.__clinica.obtener_medicos()
        if not medicos:
            print("No hay médicos registrados en el sistema.")
        else:
            for i, medico in enumerate(medicos):
                print(f"\n--- Médico {i+1} ---")
                print(medico)
        self._pausar_pantalla()

    # --- Flujo Principal ---

    def iniciar(self):
        while True:
            self._mostrar_menu()
            opcion = input("Elige una opción: ").strip()

            if opcion == '1': self._agregar_paciente()
            elif opcion == '2': self._agregar_medico()
            elif opcion == '3': self._agendar_turno()
            elif opcion == '4': self._agregar_especialidad_a_medico()
            elif opcion == '5': self._emitir_receta()
            elif opcion == '6': self._ver_historia_clinica()
            elif opcion == '7': self._ver_todos_los_turnos()
            elif opcion == '8': self._ver_todos_los_pacientes()
            elif opcion == '9': self._ver_todos_los_medicos()
            elif opcion == '0':
                print("\n¡Gracias por usar el sistema de la Clínica! ¡Hasta pronto!")
                break
            else:
                print("\nOpción no válida. Por favor, elige un número del menú.")
                self._pausar_pantalla()
