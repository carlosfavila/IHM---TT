# Interfaz IHM (Tkinter) - Estado actual

Esta interfaz está pensada para ejecutarse en una pantalla táctil de **7"** con ventana fija de **800x480**.

## Qué se muestra en el menú principal

Al iniciar se limpia la ventana y se presenta un **header** con:

- Logotipo de `ipn.png` (izquierda)
- Título en **2 líneas**
- Subtítulo `UPIITA - IPN`
- Logotipo de `UPIITA.png` (derecha)

Debajo del header aparecen dos botones centrados:

- `CARGAR`
- `MANUAL`

## Pantalla `CARGAR`

Al entrar a `CARGAR` se muestra el texto `CARGAR` y un botón grande cuyo comportamiento es:

1. Se inicia con el texto `CARGANDO` y fondo rojo (`#c71414`).
2. Al presionarlo estando en `CARGANDO`:
   - Cambia a color rojo.
   - Se deshabilita la acción del botón (queda como “bloqueado”).
3. Después de 4 segundos, el botón cambia automáticamente a:
   - Texto `COLOCAR`
   - Fondo azul (`#104ba3`)

> Nota: en el código actual, en la transición desde `COLOCAR` hacia `COLOCANDO` se llama a `handle_btncolocar_click(...)`, pero esa función no existe en el archivo. Si vas a probar la parte `COLOCAR`, ahí puede fallar o no hacer lo esperado.

## Pantalla `MANUAL`

En `MANUAL` se eliminan los botones grandes/extra y se dejan **solo 6 pares** de controles, uno por cada grado de libertad de un robot **6GDL**.

Para cada `Grado N` (N de 1 a 6) hay:

- Botón `+`
- Botón `-`

Cada `+` o `-` envía un **vector de 6 valores** por nRF24:

- Si presionas `+` del `Grado N`, el vector enviado es `0,0,...,+1,...,0`
- Si presionas `-` del `Grado N`, el vector enviado es `0,0,...,-1,...,0`

Ejemplo (como lo pediste):

- `Grado 3` `+` -> `0,0,+1,0,0,0`
- `Grado 3` `-` -> `0,0,-1,0,0,0`

También se tiene disponible el botón `Menú Principal` para regresar.

## Comunicación nRF24L01 (RX/TX)

En `IHM.py` se agregó soporte para nRF24L01 usando la librería Python `RF24`.

Configuración (tal cual está en el archivo):

- `CE_PIN = 22`
- `CSN_PIN = 0`
- `CHANNEL = 76`
- `ADDRESS = b"00001"`
- Data rate: `RF24_250KBPS`
- PA level: `RF24_PA_HIGH`
- CRC: `RF24_CRC_16`

### RX (recepción)

Se crea un hilo en segundo plano que escucha el radio:

- Cuando recibe datos, imprime en consola `<= RX: <mensaje>`
- Se reinicia el modo listening de forma periódica para estabilizar recepción.

### TX (envío)

Cuando presionas `+` o `-` en `MANUAL`, la interfaz:

1. Genera el vector de 6 valores.
2. Lo convierte a una **cadena UTF-8 con comas** (ej. `0,0,+1,0,0,0`).
3. Ejecuta TX y reinicia `startListening()` para continuar RX.

## Recursos necesarios en la carpeta del programa

Este programa usa:

- `ipn.png`
- `UPIITA.png`

La imagen `k.jpg` fue eliminada de la interfaz (antes aparecía en todas las pantallas).

