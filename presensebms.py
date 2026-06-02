import sys
import asyncio
import time
import subprocess
import ctypes
import ctypes.wintypes
from pypresence import Presence

# 1. Parche de compatibilidad para Python 3.13 en Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# 2. Definición de la estructura exacta de BMS 4.37 (usando solo los valores necesarios)
class FlightData(ctypes.Structure):
    _fields_ = [
        ("padding0", ctypes.c_float * 2),  # x, y
        ("z", ctypes.c_float),              # Altitud (Eje Z)
        ("padding1", ctypes.c_float * 9),   # xDot, yDot, zDot, alpha, beta, gamma, pitch, roll, yaw
        ("kias", ctypes.c_float),           # Indicada
        ("vt", ctypes.c_float),             # Velocidad Verdadera / Total
        ("gs", ctypes.c_float),             # Ground Speed
    ]

# Nombres posibles del ejecutable de BMS. Ajusta según el nombre real del proceso.
GAME_PROCESS_NAMES = [
    "Falcon BMS.exe",
]

# Nombres de proceso del launcher alternativo. Se usan para que el script permanezca vivo mientras
# el launcher está abierto y está esperando a que aparezca Falcon BMS.exe.
WAIT_PROCESS_NAMES = [
    "FalconBMS_Alternative_Launcher.exe",
]

# Estructura extendida para obtener la posición en tierra
class FalconSharedMemory:
    def __init__(self):
        self.handle = None
        self.view = None
        
    def connect(self):
        # Intentar abrir el área de memoria compartida nativa de BMS
        try:
            # Constante de Windows para abrir archivos mapeados
            FILE_MAP_READ = 0x0004
            ctypes.windll.kernel32.OpenFileMappingW.restype = ctypes.wintypes.HANDLE
            self.handle = ctypes.windll.kernel32.OpenFileMappingW(FILE_MAP_READ, False, "FalconSharedMemoryArea")
            
            if self.handle:
                ctypes.windll.kernel32.MapViewOfFile.restype = ctypes.c_void_p
                self.view = ctypes.windll.kernel32.MapViewOfFile(self.handle, FILE_MAP_READ, 0, 0, 0)
                return True
        except Exception:
            pass
        return False

    def get_data(self):
        if not self.view:
            return None
        # Casteamos los bytes de la memoria a nuestra estructura legible de Python
        return FlightData.from_address(self.view)

    def close(self):
        if self.view:
            ctypes.windll.kernel32.UnmapViewOfFile(ctypes.c_void_p(self.view))
            self.view = None
        if self.handle:
            ctypes.windll.kernel32.CloseHandle(self.handle)
            self.handle = None


def is_process_running(names):
    try:
        result = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            shell=False,
        )
        if result.returncode != 0:
            return False

        expected_names = {name.lower() for name in names}
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            process_name = line.split('","')[0].strip('"').lower()
            if process_name in expected_names:
                return True

        return False
    except Exception:
        return False


def is_game_running():
    return is_process_running(GAME_PROCESS_NAMES)


def is_wait_process_running():
    return is_process_running(WAIT_PROCESS_NAMES)

# 3. Configuración de Discord
CLIENT_ID = "CLIENT DISCORD ID"  # Pon tu ID de Discord aquí
UPDATE_INTERVAL = 5  # segundos entre actualizaciones a Discord
RPC = Presence(CLIENT_ID)

print("Conectando con Discord...")
try:
    RPC.connect()
    print("¡Discord conectado!")
except Exception as e:
    print(f"Error al conectar con Discord: {e}")
    sys.exit(1)

# Instanciamos el lector de memoria
bms_memory = FalconSharedMemory()
print("\nBuscando Falcon BMS 4.37 en ejecución... (Asegúrate de estar en cabina 3D)")

start_time = time.time()
in_game_previously = False

try:
    while True:
        # Intentamos conectar a la memoria si no estamos conectados
        if not bms_memory.view:
            bms_memory.connect()
            
        data = bms_memory.get_data()
        
        if data:
            if not in_game_previously:
                start_time = time.time()
                in_game_previously = True
                print("¡Falcon BMS 4.37 detectado con éxito! Leyendo telemetría...")

            # --- CORRECCIÓN DE TELEMETRÍA ---
            if data.kias > 1:
                nudos = int(data.kias)
            elif data.vt > 1:
                nudos = int(data.vt if data.vt <= 500 else data.vt / 1.68781)
            else:
                nudos = 0

            altitud = int(abs(data.z))
            
            if nudos > 2500:
                nudos = 0
            if altitud > 100000:
                altitud = 0

            # Si estamos alto en el aire, no se considera taxi aunque la velocidad leída sea baja.
            en_el_aire = nudos > 30 or altitud > 1000

            if en_el_aire:
                situacion = "En el Aire"
                estado = f"{nudos} KTS | ALT: {altitud:,} FT"
            else:
                situacion = "En Tierra / Rampa"
                estado = f"Pre-flight / Taxi | {nudos} KTS"

            detalles = f"Falcon BMS 4.37 ({situacion})"

            RPC.update(
                details=detalles,
                state=estado,
                start=start_time,
                large_image="bms_logo",      
                large_text="Falcon BMS 4.37",
                small_image="f16",           
                small_text="Viper Driver"
            )
        else:
            if in_game_previously:
                print("Se cerró el simulador o saliste al menú UI. Limpiando presencia...")
                RPC.clear()
                bms_memory.close()
                in_game_previously = False
                if is_wait_process_running():
                    print("FalconBMS Alternative Launcher detectado. Esperando Falcon BMS.exe...")

        if in_game_previously and not (is_game_running() or is_wait_process_running()):
            print("El juego ya no está en ejecución. Saliendo del script...")
            break

        time.sleep(UPDATE_INTERVAL)  # Intervalo de actualización a Discord

except KeyboardInterrupt:
    print("\nCerrando el script protector...")
    bms_memory.close()
    RPC.close()