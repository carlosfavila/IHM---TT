import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import time

try:
    # Librería para nRF24L01 en Raspberry Pi
    from RF24 import RF24, RF24_PA_HIGH, RF24_250KBPS, RF24_CRC_16
    RF24_AVAILABLE = True
except Exception:
    RF24_AVAILABLE = False

colocado = 0

# ===================== nRF24L01 Config =====================
CE_PIN = 22
CSN_PIN = 0
CHANNEL = 76
ADDRESS = b"00001"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz Humano Máquina de Brazo Robótico")
        #self.geometry("1920x1080")
        self.geometry("800x480")
        self.configure(bg="#051d40")
        self.create_main_menu()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Inicialización de comunicación nRF24L01 (si está disponible)
        self.radio_lock = threading.Lock()
        self.radio = None
        self._radio_stop_event = threading.Event()
        self._radio_thread = None
        self._init_radio()

    def on_close(self):
        # Detener hilo RX antes de cerrar
        self._radio_stop_event.set()
        if self._radio_thread and self._radio_thread.is_alive():
            self._radio_thread.join(timeout=1.0)
        self.destroy()

    def _init_radio(self):
        if not RF24_AVAILABLE:
            print("RF24 no disponible. TX/RX deshabilitado.")
            return

        try:
            self.radio = RF24(CE_PIN, CSN_PIN)
            if not self.radio.begin():
                raise RuntimeError("No se pudo inicializar el nRF24L01")

            self.radio.setChannel(CHANNEL)
            self.radio.setDataRate(RF24_250KBPS)
            self.radio.setPALevel(RF24_PA_HIGH)
            self.radio.setAutoAck(True)
            self.radio.enableDynamicPayloads()
            self.radio.setCRCLength(RF24_CRC_16)
            self.radio.openWritingPipe(ADDRESS)
            self.radio.openReadingPipe(1, ADDRESS)
            self.radio.flush_rx()
            self.radio.flush_tx()
            self.radio.startListening()

            print("=== nRF24L01 listo ===")
            print(f"Canal: {CHANNEL}, Address: {ADDRESS}")

            self._radio_thread = threading.Thread(target=self._radio_rx_loop, daemon=True)
            self._radio_thread.start()
        except Exception as e:
            self.radio = None
            print(f"Error inicializando RF24: {e}")

    def _radio_rx_loop(self):
        # Mantiene una escucha continua; en cuanto llega algo lo imprime.
        while not self._radio_stop_event.is_set():
            try:
                with self.radio_lock:
                    if self.radio is not None and self.radio.available():
                        # Vaciar buffer
                        while self.radio.available():
                            size = self.radio.getDynamicPayloadSize()
                            if 0 < size <= 32:
                                data = self.radio.read(size)
                                try:
                                    msg = data.decode("utf-8", errors="replace")
                                    print(f"[{time.strftime('%H:%M:%S')}] <= RX: {msg}")
                                except Exception:
                                    pass
                            else:
                                break

                        # Reinicio "crítico" para estabilizar recepción
                        self.radio.stopListening()
                        time.sleep(0.01)
                        self.radio.flush_rx()
                        self.radio.startListening()

                time.sleep(0.01)
            except Exception as e:
                print(f"Error en hilo RX: {e}")
                time.sleep(0.25)

    def _send_vector_6dof(self, vector_6):
        if self.radio is None:
            return False

        # vector_6 debe ser una lista de 6 enteros (-1,0,1)
        payload_parts = []
        for v in vector_6:
            if v > 0:
                payload_parts.append(f"+{v}")
            else:
                payload_parts.append(str(v))

        text = ",".join(payload_parts)
        payload = text.encode("utf-8")

        with self.radio_lock:
            # Secuencia TX tomada del código base
            self.radio.stopListening()
            time.sleep(0.01)
            self.radio.flush_tx()
            ok = self.radio.write(payload)
            print(f"[{time.strftime('%H:%M:%S')}] => TX (ok={ok}): {text}")
            time.sleep(0.01)
            self.radio.flush_rx()
            self.radio.startListening()

        return ok

    def _send_home(self):
        """Envía el comando HOME para regresar todos los motores a 0°."""
        if self.radio is None:
            print("HOME: radio no disponible")
            return False
        with self.radio_lock:
            self.radio.stopListening()
            time.sleep(0.01)
            self.radio.flush_tx()
            ok = self.radio.write(b"HOME")
            print(f"[{time.strftime('%H:%M:%S')}] => TX HOME (ok={ok})")
            time.sleep(0.01)
            self.radio.flush_rx()
            self.radio.startListening()
        return ok

    def create_main_menu(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        # Encabezado con imágenes
        header_frame = tk.Frame(self, bg="#051d40")
        header_frame.pack(pady=0)

        img1 = Image.open("ipn.png")
        img1 = img1.resize((60, 72))
        img1 = ImageTk.PhotoImage(img1)
        img_label1 = tk.Label(header_frame, image=img1, background="#051d40")
        img_label1.image = img1
        img_label1.pack(side=tk.LEFT)

        # Frame para los textos (Título y Subtítulo)
        text_frame = tk.Frame(header_frame, bg="#051d40")
        text_frame.pack(side=tk.LEFT, padx=24)

        header_label = tk.Label(
            text_frame,
            text="Brazo robótico orientado a auxiliar\nseres humanos en la exploración planetaria",
            font=("Montserrat", 20),
            bg="#051d40",
            fg="#ffffff",
            justify="center"
        )
        header_label.pack()

        subtitle_label = tk.Label(text_frame, text="UPIITA - IPN", font=("Montserrat", 14), bg="#051d40", fg="#ffffff")
        subtitle_label.pack()

        img2 = Image.open("UPIITA.png")
        img2 = img2.resize((60, 60))
        img2 = ImageTk.PhotoImage(img2)
        img_label2 = tk.Label(header_frame, image=img2, background="#051d40")
        img_label2.image = img2
        img_label2.pack(side=tk.LEFT)

        # Botones
        button_frame = tk.Frame(self, bg="#051d40")
        button_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Estilo para botones ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#104ba3", foreground="#ffffff", font=("Montserrat", 18), borderwidth=0, width=40)
        style.map("TButton", background=[("active", "#65a3ff")])

        btn1 = ttk.Button(button_frame, text="CARGAR", command=self.show_screen1)
        btn1.pack(pady=20)

        btn2 = ttk.Button(button_frame, text="MANUAL", command=self.show_screen2)
        btn2.pack(pady=20)

    def show_screen1(self):
        self.show_screen("CARGAR")

    def show_screen2(self):
        self.show_screen("MANUAL")

    def create_manual_controls(self, parent_frame):
        # Configurar 7 filas: 6 GDL + 1 HOME
        for i in range(7):
            parent_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            parent_frame.grid_columnconfigure(j, weight=1)

        for i in range(6):
            grado_num = i + 1

            label = tk.Label(
                parent_frame,
                text=f"Grado {grado_num}",
                bg="#051d40",
                fg="#ffffff",
                font=("Montserrat Bold", 16)
            )
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            btn_menos = tk.Button(
                parent_frame,
                text="-",
                width=4,
                height=1,
                bg="#104ba3",
                fg="#ffffff",
                font=("Montserrat Bold", 16),
                command=lambda n=grado_num: self.on_manual_click(n, -1)
            )
            btn_menos["borderwidth"] = 0
            btn_menos["activebackground"] = "#65a3ff"
            btn_menos.grid(row=i, column=1, padx=10, pady=10, sticky="e")

            btn_mas = tk.Button(
                parent_frame,
                text="+",
                width=4,
                height=1,
                bg="#104ba3",
                fg="#ffffff",
                font=("Montserrat Bold", 16),
                command=lambda n=grado_num: self.on_manual_click(n, 1)
            )
            btn_mas["borderwidth"] = 0
            btn_mas["activebackground"] = "#65a3ff"
            btn_mas.grid(row=i, column=2, padx=10, pady=10, sticky="w")

        # Botón HOME - fila 6, ocupa las 3 columnas
        btn_home = tk.Button(
            parent_frame,
            text="HOME",
            width=12,
            height=1,
            bg="#c71414",
            fg="#ffffff",
            font=("Montserrat Bold", 16),
            command=self._send_home
        )
        btn_home["borderwidth"] = 0
        btn_home["activebackground"] = "#ff4444"
        btn_home.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def on_manual_click(self, grado, direccion):
        # vector de 6 valores: 1 si aumenta, -1 si disminuye, 0 si no aplica
        # Ejemplo (grado 3, +): 0,0,+1,0,0,0
        vector = [0, 0, 0, 0, 0, 0]
        idx = int(grado) - 1
        if 0 <= idx < 6:
            vector[idx] = int(direccion)
        else:
            return

        sentido = "+" if direccion > 0 else "-"
        print(f"Grado {grado} movido en sentido {sentido} -> enviando {vector}")
        self._send_vector_6dof(vector)

    def handle_btncarga_click(self, btncarga):
        if btncarga["text"] == "CARGANDO":
            btncarga.config(bg="#c71414")
            btncarga.config(command=lambda: None)  # Deshabilitar el botón
        if btncarga["text"] == "COLOCAR":
            btncarga.config(text="COLOCANDO", bg="#c71414")  # Cambiar el color al presionar
            btncarga.config(command=lambda: self.handle_btncolocar_click(btncarga))
            print("Botón COLOCAR presionado")
            btncarga.after(4000, lambda: btncarga.config(text="COLOCADO", bg="#65a3ff",command=lambda: None))
            

    def show_screen(self, screen_name):
        # Limpiar la pantalla
        for widget in self.winfo_children():
            widget.destroy()

        screen_label = tk.Label(self, text=screen_name, font=("Montserrat Bold", 24), bg="#051d40", fg="#ffffff")
        screen_label.pack(pady=20)

        # Frame para botones
        button_frame = tk.Frame(self, bg="#051d40")
        button_frame.pack(expand=True, fill="both", padx=40, pady=40)

        if screen_name == "MANUAL":
            self.create_manual_controls(button_frame)

        if screen_name == "CARGAR":
            texto = "CARGANDO"
            backgr = "#c71414"
            btncarga = tk.Button(
                button_frame,
                text=texto,
                bg=backgr,
                fg="#ffffff",
                font=("Montserrat Bold", 15),
                width=20,
                command=lambda: self.handle_btncarga_click(btncarga)  # Asignar la función al clic
            )
            btncarga.pack(pady=0)
            btncarga["borderwidth"] = 0

            # Cambiar a "COLOCAR" después de 4 segundos
            btncarga.after(4000, lambda: btncarga.config(text="COLOCAR", bg="#104ba3"))

        # Botón "Menú Principal"
        back_button = ttk.Button(self, text="Menú Principal", command=self.create_main_menu)
        back_button.pack(side=tk.LEFT, anchor="s", padx=200, pady=10)


if __name__ == "__main__":
    app = App()
    icon_path = os.path.join(os.path.dirname(__file__), "robot.ico")
#    app.iconbitmap(icon_path)
    app.mainloop()