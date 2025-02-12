import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz Humano Máquina de Brazo Robótico")
        self.geometry("1300x600")
        self.configure(bg="#051d40")
        
        self.create_main_menu()

    def create_main_menu(self):
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()

        # Header with images
        header_frame = tk.Frame(self, bg="#051d40")
        header_frame.pack(pady=0)

        img1 = Image.open("ipn.png")
        img1 = img1.resize((60,80))
        img1 = ImageTk.PhotoImage(img1)
        img_label1 = tk.Label(header_frame, image=img1,background="#051d40")
        img_label1.image = img1
        img_label1.pack(side=tk.LEFT)

        # Nuevo Frame para los textos (Título y Subtítulo)
        text_frame = tk.Frame(header_frame)
        text_frame["bg"] = "#051d40"
        text_frame.pack(side=tk.LEFT, padx=20)  # Se mantiene alineado a la izquierda

        header_label = tk.Label(text_frame, text="Brazo robótico orientado a auxiliar seres humanos en la exploración planetaria ", font=("Montserrat", 24))
        header_label["bg"] = "#051d40"
        header_label["fg"] = "#ffffff"
        header_label.pack()

        subtitle_label = tk.Label(text_frame, text="UPIITA - IPN", font=("Montserrat", 16))
        subtitle_label["bg"] = "#051d40"
        subtitle_label["fg"] = "#ffffff"
        subtitle_label.pack()

        img2 = Image.open("UPIITA.png")
        img2 = img2.resize((80, 80))
        img2 = ImageTk.PhotoImage(img2)
        img_label2 = tk.Label(header_frame, image=img2,background="#051d40")
        img_label2.image = img2
        img_label2.pack(side=tk.LEFT)

        # Left image
        left_img = Image.open("k.jpg")
        left_img = left_img.resize((800, 600))
        left_img = ImageTk.PhotoImage(left_img)
        left_img_label = tk.Label(self, image=left_img, borderwidth=0)
        left_img_label.image = left_img
        left_img_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=20, pady=20)
        button_frame["bg"] = "#051d40"

        # Crear estilo para botones ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#104ba3", foreground="#ffffff"
                        , font=("Montserrat", 12), borderwidth=0, width=30)
        style.map("TButton", background=[("active", "#65a3ff")])  # Cambio al presionar

        btn1 = ttk.Button(button_frame, text="CARGAR", command=self.show_screen1)
        btn1.pack(pady=10)

        btn2 = ttk.Button(button_frame, text="ATORNILLAR", command=self.show_screen2)
        btn2.pack(pady=10)

        btn3 = ttk.Button(button_frame, text="ESCRIBIR", command=self.show_screen3)
        btn3.pack(pady=10)

    def show_screen1(self):
        self.show_screen("CARGAR")

    def show_screen2(self):
        self.show_screen("ATORNILLAR")

    def show_screen3(self):
        self.show_screen("ESCRIBIR")

    def show_screen(self, screen_name):
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()

        screen_label = tk.Label(self, text=screen_name, font=("Montserrat", 24))
        screen_label["bg"] = "#051d40"
        screen_label["fg"] = "#ffffff"
        screen_label.pack(pady=20)

        # Left image
        left_img = Image.open("k.jpg")
        left_img = left_img.resize((800, 600))
        left_img = ImageTk.PhotoImage(left_img)
        left_img_label = tk.Label(self, image=left_img, borderwidth=0)
        left_img_label.image = left_img
        left_img_label.pack(side=tk.LEFT, padx=20, pady=20)

        back_button = ttk.Button(self, text="Menú Principal", command=self.create_main_menu)
        back_button.pack(pady=20)

if __name__ == "__main__":
    app = App()
   # icon_path = os.path.join(os.path.dirname(__file__), "robot.ico")
   # app.iconbitmap(icon_path)
    app.mainloop()
