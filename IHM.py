import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

colocado = 0

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz Humano Máquina de Brazo Robótico")
        self.geometry("1920x1080")
        self.configure(bg="#051d40")
        self.create_main_menu()

    def create_main_menu(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        # Encabezado con imágenes
        header_frame = tk.Frame(self, bg="#051d40")
        header_frame.pack(pady=0)

        img1 = Image.open("ipn.png")
        img1 = img1.resize((100, 120))
        img1 = ImageTk.PhotoImage(img1)
        img_label1 = tk.Label(header_frame, image=img1, background="#051d40")
        img_label1.image = img1
        img_label1.pack(side=tk.LEFT)

        # Frame para los textos (Título y Subtítulo)
        text_frame = tk.Frame(header_frame, bg="#051d40")
        text_frame.pack(side=tk.LEFT, padx=24)

        header_label = tk.Label(text_frame, text="Brazo robótico orientado a auxiliar seres humanos en la exploración planetaria", font=("Montserrat", 28), bg="#051d40", fg="#ffffff")
        header_label.pack()

        subtitle_label = tk.Label(text_frame, text="UPIITA - IPN", font=("Montserrat", 20), bg="#051d40", fg="#ffffff")
        subtitle_label.pack()

        img2 = Image.open("UPIITA.png")
        img2 = img2.resize((100, 100))
        img2 = ImageTk.PhotoImage(img2)
        img_label2 = tk.Label(header_frame, image=img2, background="#051d40")
        img_label2.image = img2
        img_label2.pack(side=tk.LEFT)

        # Imagen izquierda
        left_img = Image.open("k.jpg")
        left_img = left_img.resize((1100, 800))
        left_img = ImageTk.PhotoImage(left_img)
        left_img_label = tk.Label(self, image=left_img, borderwidth=0)
        left_img_label.image = left_img
        left_img_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Botones
        button_frame = tk.Frame(self, bg="#051d40")
        button_frame.pack(expand=True, padx=20, pady=20)

        # Estilo para botones ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#104ba3", foreground="#ffffff", font=("Montserrat", 18), borderwidth=0, width=40)
        style.map("TButton", background=[("active", "#65a3ff")])

        btn1 = ttk.Button(button_frame, text="CARGAR", command=self.show_screen1)
        btn1.pack(pady=10)

        btn2 = ttk.Button(button_frame, text="PUNTOS", command=self.show_screen2)
        btn2.pack(pady=10)

    def show_screen1(self):
        self.show_screen("CARGAR")

    def show_screen2(self):
        self.show_screen("PUNTOS")

    def create_button_grid(self, parent_frame):
        rows = 5
        cols = 5
        for i in range(rows):
            for j in range(cols):
                button_number = i * cols + j + 1
                button = tk.Button(
                    parent_frame,
                    text=str(button_number),
                    width=6,
                    height=2,
                    bg="#104ba3",
                    fg="#ffffff",
                    font=("Montserrat Bold", 15),
                    command=lambda num=button_number: self.on_button_click(num)
                )
                button["borderwidth"] = 0
                button["activebackground"] = "#65a3ff"
                button.grid(row=i, column=j, padx=5, pady=5)

    def on_button_click(self, button_number):
        print(f"Botón {button_number} presionado")

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

       # Imagen izquierda
        left_img = Image.open("k.jpg")
        left_img = left_img.resize((1100, 800))
        left_img = ImageTk.PhotoImage(left_img)
        left_img_label = tk.Label(self, image=left_img, borderwidth=0)
        left_img_label.image = left_img
        left_img_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Frame para botones
        button_frame = tk.Frame(self, bg="#051d40")
        button_frame.pack(expand=True, padx=20, pady=20)

        if screen_name == "PUNTOS":
            self.create_button_grid(button_frame)

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