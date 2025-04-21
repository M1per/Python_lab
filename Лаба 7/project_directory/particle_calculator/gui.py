import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .particles import Electron, Proton, Neutron
from .file_operations import DocxSaver, XlsxSaver


class ParticleCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор частиц")
        self.particles = {
            "Электрон": Electron(),
            "Протон": Proton(),
            "Нейтрон": Neutron()
        }
        self.current_particle = None
        self.data = {}
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="Выберите частицу:").grid(row=0, column=0, padx=5, pady=5)
        self.particle_var = tk.StringVar(value="Электрон")
        ttk.Combobox(
            self.root,
            textvariable=self.particle_var,
            values=list(self.particles.keys())
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Рассчитать", command=self.calculate).grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(self.root, text="Удельный заряд:").grid(row=2, column=0, sticky="w", padx=5)
        self.sc_label = ttk.Label(self.root, text="")
        self.sc_label.grid(row=2, column=1, sticky="w", padx=5)

        ttk.Label(self.root, text="Длина волны:").grid(row=3, column=0, sticky="w", padx=5)
        self.wl_label = ttk.Label(self.root, text="")
        self.wl_label.grid(row=3, column=1, sticky="w", padx=5)

        ttk.Button(self.root, text="Сохранить DOCX", command=lambda: self.save(DocxSaver())).grid(row=4, column=0,
                                                                                                  pady=10)
        ttk.Button(self.root, text="Сохранить XLSX", command=lambda: self.save(XlsxSaver())).grid(row=4, column=1,
                                                                                                  pady=10)

    def calculate(self):
        particle = self.particles[self.particle_var.get()]
        self.data = {
            "Частица": particle.name,
            "Удельный заряд": f"{particle.calculate_specific_charge():.4e} Кл/кг",
            "Длина волны": f"{particle.calculate_compton_wavelength():.4e} м"
        }
        self.sc_label.config(text=self.data["Удельный заряд"])
        self.wl_label.config(text=self.data["Длина волны"])

    def save(self, saver):
        if not self.data:
            messagebox.showwarning("Ошибка", "Сначала выполните расчет")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=saver.default_ext,
            filetypes=[(saver.file_type, f"*{saver.default_ext}")]
        )
        if filename:
            saver.save(filename, self.data)
            messagebox.showinfo("Успех", "Файл сохранен")