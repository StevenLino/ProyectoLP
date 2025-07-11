import tkinter as tk
from tkinter import filedialog, PhotoImage
from analizadores import analizar_lexico, analizar_sintactico, analizar_semantico

# Editor con numeración de líneas
class LineNumberedText(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.text = tk.Text(self, **kwargs, bg="black", fg="white", insertbackground="white", wrap=tk.NONE)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.linenumbers = tk.Canvas(self, width=40, bg="#222222", highlightthickness=0)
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text.bind("<KeyRelease>", self._update_line_numbers)
        self.text.bind("<MouseWheel>", self._update_line_numbers)
        self.text.bind("<ButtonRelease>", self._update_line_numbers)
        self.text.bind("<Configure>", self._update_line_numbers)

        self._update_line_numbers()

    def _update_line_numbers(self, event=None):
        self.linenumbers.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.linenumbers.create_text(2, y, anchor="nw", text=linenum, fill="white", font=("Consolas", 10))
            i = self.text.index(f"{i}+1line")

    # Métodos que se reenvían al Text interno
    def get(self, *args):
        return self.text.get(*args)

    def delete(self, *args):
        return self.text.delete(*args)

    def insert(self, *args):
        return self.text.insert(*args)

    def bind(self, *args):
        return self.text.bind(*args)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)

    def configure(self, *args, **kwargs):
        self.text.configure(*args, **kwargs)

    def index(self, index):
        return self.text.index(index)


# === Interfaz principal ===
class AnalizadorRubyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Ruby")
        self.root.geometry("900x600")
        self.root.configure(bg="#732F42")
        self.create_widgets()

    def create_widgets(self):
        # ==== Menú superior ====
        frame_superior = tk.Frame(self.root, bg="#5A1E2B", height=50)
        frame_superior.pack(fill=tk.X)

        estilo_boton = {"cursor": "hand2"}

        btn_abrir = tk.Button(frame_superior, text="Abrir archivo", bg="#C76C52", fg="white", command=self.abrir_archivo, **estilo_boton)
        btn_abrir.pack(side=tk.LEFT, padx=20, pady=10)

        btn_guardar = tk.Button(frame_superior, text="Guardar archivo", bg="#C76C52", fg="white", command=self.guardar_archivo, **estilo_boton)
        btn_guardar.pack(side=tk.LEFT, padx=10, pady=10)

        # === Ícono Ruby y texto ===
        self.ruby_icon = tk.PhotoImage(file="ruby_icon.png").subsample(96, 96)
        ruby_frame = tk.Frame(frame_superior, bg="#5A1E2B")
        ruby_frame.pack(side=tk.RIGHT, padx=10)
        tk.Label(ruby_frame, text="Ruby", fg="white", bg="#5A1E2B", font=("Arial", 16, "italic")).pack(side=tk.LEFT, padx=5)
        tk.Label(ruby_frame, image=self.ruby_icon, bg="#5A1E2B").pack(side=tk.LEFT)

        # ==== Cuerpo principal ====
        frame_principal = tk.Frame(self.root, bg="#823B4A")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Editor de código ===
        frame_editor = tk.Frame(frame_principal, bg="#823B4A")
        frame_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(frame_editor, text="Editor de código:", bg="#823B4A", fg="white").pack(anchor="w")
        self.editor = LineNumberedText(frame_editor)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # === Consola de salida (solo lectura) ===
        frame_consola = tk.Frame(frame_principal, bg="#823B4A")
        frame_consola.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(frame_consola, text="Consola de salida:", bg="#823B4A", fg="white").pack(anchor="w")
        self.consola = tk.Text(frame_consola, wrap=tk.WORD, bg="white", fg="black", state="disabled")
        self.consola.pack(fill=tk.BOTH, expand=True)

        # ==== Botones inferiores ====
        frame_botones = tk.Frame(self.root, bg="#823B4A", height=50)
        frame_botones.pack(fill=tk.X, pady=10)

        estilo_boton = { "cursor": "hand2"}

        tk.Button(frame_botones, text="Borrar", bg="#C76C52", fg="white", command=self.borrar_todo, **estilo_boton).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Análisis léxico", bg="#C76C52", fg="white", command=self.analisis_lexico, **estilo_boton).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Análisis sintáctico", bg="#C76C52", fg="white", command=self.analisis_sintactico, **estilo_boton).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Análisis semántico", bg="#C76C52", fg="white", command=self.analisis_semantico, **estilo_boton).pack(side=tk.LEFT, padx=10)

    # ==== Función auxiliar para la consola ====
    def mostrar_en_consola(self, texto):
        self.consola.config(state="normal")
        self.consola.delete("1.0", tk.END)
        self.consola.insert(tk.END, texto)
        self.consola.config(state="disabled")

    # ==== Funciones ====
    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Ruby", "*.rb")])
        if ruta:
            with open(ruta, 'r', encoding='utf-8') as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, f.read())

    def guardar_archivo(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".rb", filetypes=[("Archivos Ruby", "*.rb")])
        if ruta:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(self.editor.get("1.0", tk.END))

    def borrar_todo(self):
        self.editor.delete("1.0", tk.END)
        self.mostrar_en_consola("")

    def analisis_lexico(self):
        codigo = self.editor.get("1.0", tk.END)
        resultado = analizar_lexico(codigo)
        self.mostrar_en_consola(resultado)

    def analisis_sintactico(self):
        codigo = self.editor.get("1.0", tk.END)
        resultado = analizar_sintactico(codigo)
        self.mostrar_en_consola(resultado)

    def analisis_semantico(self):
        codigo = self.editor.get("1.0", tk.END)
        resultado = analizar_semantico(codigo)
        self.mostrar_en_consola(resultado)


# ==== Lanzamiento de la app ====
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorRubyApp(root)
    root.mainloop()
