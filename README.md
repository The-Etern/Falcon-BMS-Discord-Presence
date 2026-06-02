# Falcon-BMS-Discord-Presence

Una herramienta que muestra tu actividad en Falcon BMS 4.37 en Discord Rich Presence con detalles en tiempo real.

## 📋 Requisitos
- Python 3.8+
- Windows (usa APIs nativas de Windows)
- Falcon BMS 4.37 instalado y funcional
- Una cuenta de Discord

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/The-Etern/Falcon-BMS-Discord-Presence
cd Falcon-BMS-Discord-Presence
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración Paso a Paso

### Paso 1: Obtener el Discord Client ID

1. **Accede al Discord Developer Portal**
   - Ve a https://discord.com/developers/applications
   - Inicia sesión con tu cuenta de Discord

2. **Crea una nueva aplicación**
   - Haz clic en el botón "New Application" (en la esquina superior derecha)
   - Dale un nombre (ej: "Falcon BMS Presence")
   - Acepta los términos y crea la aplicación

3. **Obtén tu Client ID**
   - En la sección "General Information", verás tu **Client ID**
   - Haz clic en "Copy" para copiar el ID
   - Guarda este número, lo necesitarás en el siguiente paso

4. **Configura las imágenes (Opcional)**
   - Ve a la sección "Art Assets" en el menú lateral
   - Sube las imágenes para los Rich Presence:
     - `bms_logo` - Logo principal (512x512 px recomendado)
     - `f16` - Imagen pequeña (512x512 px recomendado)
   - Estos nombres se usan en el script (líneas 168-171)

### Paso 2: Configurar el Script

1. **Edita `presensebms.py`**
   - Abre el archivo en tu editor favorito
   - Busca la línea 104: `CLIENT_ID = "CLIENT DISCORD ID"`
   - Reemplaza `"CLIENT DISCORD ID"` con tu Client ID copiado:
   ```python
   CLIENT_ID = "1234567890123456789"  # Tu Client ID aquí
   ```

2. **Configurar la ruta del juego (Opcional)**
   - Si usas el launcher alternativo de Falcon BMS, asegúrate de que esté instalado
   - El script detectará automáticamente los procesos:
     - `Falcon BMS.exe` - Simulador principal
     - `FalconBMS_Alternative_Launcher.exe` - Launcher alternativo
   - Si el nombre del ejecutable es diferente, edita las líneas 25-26 y 31-33

## ▶️ Uso

### Método 1: Ejecutar el Script Directamente
1. Abre una terminal en la carpeta del proyecto
2. Asegúrate de estar en la **cabina 3D de Falcon BMS 4.37**
3. Ejecuta el script:
```bash
python presensebms.py
```
4. Deberías ver el mensaje: `¡Discord conectado!`
5. Si Falcon BMS se detecta correctamente: `¡Falcon BMS 4.37 detectado con éxito! Leyendo telemetría...`

### Método 2: Usar el Batch con Permisos de Administrador
1. Haz doble clic en `launch_bms_with_presence_admin.bat`
2. Acepta el aviso de control de cuentas de usuario
3. El script se ejecutará con permisos de administrador
4. Inicia Falcon BMS 4.37 y entra a la cabina 3D

## 📊 Características

- ✈️ **Telemetría en Tiempo Real**: Velocidad (KTS) y altitud (FT)
- 🛫 **Estado Automático**: Diferencia entre vuelo y tierra/rampa
- 🔌 **Memoria Compartida**: Integración directa con Falcon BMS 4.37
- 🚀 **Compatible con Launcher**: Funciona con el launcher alternativo
- 🔄 **Actualizaciones Frecuentes**: Actualiza cada 5 segundos en Discord
- 🎨 **Rich Presence Personalizado**: Muestra imágenes y estado detallado

## 📡 Datos Que Se Muestran

| Dato | Descripción | Formato |
|------|-------------|---------|
| Estado | En el Aire / En Tierra | Texto principal |
| Velocidad | KIAS (Knots Indicated Air Speed) | KTS |
| Altitud | Altura sobre el nivel del mar | FT (pies) |
| Ground Speed | Velocidad sobre el terreno | Automático |
| Tiempo | Tiempo transcurrido en la misión | Cronómetro Discord |

### Estados Mostrados en Discord

**En el Aire:**
```
Falcon BMS 4.37 (En el Aire)
250 KTS | ALT: 5,000 FT
```

**En Tierra/Rampa:**
```
Falcon BMS 4.37 (En Tierra / Rampa)
Pre-flight / Taxi | 15 KTS
```

## 🔧 Estructura de la Telemetría

El script lee datos directamente de la memoria compartida de Falcon BMS:

```python
class FlightData(ctypes.Structure):
    - Altitud (Z): Eje Z en metros/pies
    - KIAS: Velocidad indicada
    - VT: Velocidad verdadera
    - GS: Ground speed
    - Y más...
```

**Nota**: Solo se leen los valores necesarios (KIAS, VT, GS, Altitud) para optimizar el rendimiento.

## ⚠️ Solución de Problemas

### El script no se conecta a Discord
- Verifica que tengas internet
- Asegúrate de tener Discord abierto
- Comprueba que el Client ID sea correcto

### No detecta Falcon BMS
- Asegúrate de estar en la **cabina 3D** (no en el menú UI)
- Verifica que Falcon BMS 4.37 esté realmente ejecutándose
- Ejecuta como administrador

### Error: "OpenFileMappingW failed"
- Ejecuta el script con permisos de administrador
- Asegúrate de que Falcon BMS esté en cabina 3D
- Reinicia tanto Discord como Falcon BMS

### Datos de telemetría incorrectos
- Verifica que estés en cabina 3D
- Espera 5 segundos (intervalo de actualización)
- Si persiste, reinicia Falcon BMS

## 🎮 Controles

- `Ctrl + C` - Detiene el script y limpia la presencia en Discord

## 📜 Licencia
MIT

## 👨‍💻 Autor
TheEtern

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Siéntete libre de hacer un fork y enviar pull requests.

## 📞 Soporte
Si encuentras problemas, abre un issue en el repositorio con los siguientes detalles:
- Tu versión de Python
- Tu versión de Falcon BMS
- Mensaje de error exacto
- Pasos para reproducir
