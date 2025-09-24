import os
import tkinter as tk
from tkinter import ttk, TclError
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FuzzyAutoSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Difuso de Diagnóstico Automotriz")
        self.root.state('zoomed')
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="#333333", font=("Helvetica", 10))
        style.configure("TLabelframe", background="#f0f0f0", foreground="#333", font=("Helvetica", 11, "bold"), bordercolor="#ccc")
        style.configure("TLabelframe.Label", background="#f0f0f0", foreground="#333", font=("Helvetica", 11, "bold"))
        style.configure("TScale", background="#f0f0f0")

        self._updating_from_entry = False
        self._updating_from_slider = False

        self._setup_fuzzy_system()
        self._create_widgets()
        
        self.temp_slider.set(80)
        self.presion_slider.set(55)
        self.temp_var.set(f"{self.temp_slider.get():.1f}")
        self.presion_var.set(f"{self.presion_slider.get():.1f}")
        self.update_plots()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_fuzzy_system(self):
        
        # 1. Variables de entrada y de salida (Antecedentes y Consecuente)
        self.temperatura_motor = ctrl.Antecedent(np.arange(0, 121, 1), 'temperatura_motor')
        self.presion_aceite = ctrl.Antecedent(np.arange(0, 101, 1), 'presion_aceite')
        self.accion_mecanico = ctrl.Consequent(np.arange(0, 101, 1), 'accion_mecanico')

        # 2. Definición de Funciones de Membresía
        self.temperatura_motor['frio'] = fuzz.trapmf(self.temperatura_motor.universe, [0, 0, 25, 60])
        self.temperatura_motor['normal'] = fuzz.trapmf(self.temperatura_motor.universe, [50, 70, 90, 110])
        self.temperatura_motor['caliente'] = fuzz.trapmf(self.temperatura_motor.universe, [90, 110, 120, 120])

        self.presion_aceite['baja'] = fuzz.trapmf(self.presion_aceite.universe, [0, 0, 10, 35])
        self.presion_aceite['adecuada'] = fuzz.trapmf(self.presion_aceite.universe, [25, 45, 65, 85])
        self.presion_aceite['alta'] = fuzz.trapmf(self.presion_aceite.universe, [75, 90, 100, 100])

        self.accion_mecanico['revision_rutina'] = fuzz.trapmf(self.accion_mecanico.universe, [0, 0, 20, 45])
        self.accion_mecanico['precaucion'] = fuzz.trapmf(self.accion_mecanico.universe, [35, 50, 65, 80])
        self.accion_mecanico['atencion_inmediata'] = fuzz.trapmf(self.accion_mecanico.universe, [70, 85, 100, 100])

        # 3. Reglas Difusas
        rule1 = ctrl.Rule(self.temperatura_motor['caliente'] | self.presion_aceite['baja'], self.accion_mecanico['atencion_inmediata'])
        rule2 = ctrl.Rule(self.temperatura_motor['normal'] & self.presion_aceite['adecuada'], self.accion_mecanico['revision_rutina'])
        rule3 = ctrl.Rule(self.temperatura_motor['frio'] | self.presion_aceite['alta'], self.accion_mecanico['precaucion'])

        # 4. Sistema y defuzzificación
        self.sistema_control = ctrl.ControlSystem([rule1, rule2, rule3])
        self.simulacion = ctrl.ControlSystemSimulation(self.sistema_control)

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_panel = ttk.Frame(main_frame)
        top_panel.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        controls_container = ttk.Frame(top_panel)
        controls_container.pack(fill=tk.X)
        controls_container.grid_columnconfigure(0, weight=1)
        controls_container.grid_columnconfigure(1, weight=1)

        inputs_frame = ttk.LabelFrame(controls_container, text="Controles de Simulación")
        inputs_frame.grid(row=0, column=0, sticky="nswe", padx=(0, 10))

        self.temp_var = tk.StringVar()
        self.temp_slider, self.temp_entry = self._create_slider_entry(inputs_frame, "Temperatura (°C):", 0, 120, self._on_temp_slider, self._on_temp_entry, self.temp_var)
        
        self.presion_var = tk.StringVar()
        self.presion_slider, self.presion_entry = self._create_slider_entry(inputs_frame, "Presión (PSI):", 0, 100, self._on_presion_slider, self._on_presion_entry, self.presion_var)

        result_frame = ttk.LabelFrame(controls_container, text="Resultado del Diagnóstico")
        result_frame.grid(row=0, column=1, sticky="nswe")
        result_frame.pack_propagate(False)
        result_frame.config(height=115)

        self.result_value_label = ttk.Label(result_frame, text="Valor: 0.00", font=("Helvetica", 12), anchor="center")
        self.result_value_label.pack(pady=(15, 2))
        
        self.result_text_label = ttk.Label(result_frame, text="Diagnóstico", font=("Helvetica", 14, "bold"), wraplength=280, justify=tk.CENTER, anchor="center")
        self.result_text_label.pack(pady=(2, 10), expand=True)

        plots_frame = ttk.Frame(main_frame)
        plots_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        self.fig, (self.ax_temp, self.ax_presion, self.ax_accion) = plt.subplots(1, 3, figsize=(15, 5), dpi=100)
        self.fig.patch.set_facecolor('#f0f0f0')
        self.fig.subplots_adjust(left=0.06, right=0.98, top=0.9, bottom=0.15, wspace=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plots_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def _create_slider_entry(self, parent, text, from_, to, slider_cmd, entry_cmd, var):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=10, padx=10)
        frame.grid_columnconfigure(1, weight=1)

        label = ttk.Label(frame, text=text, font=("Helvetica", 11, "bold"))
        label.grid(row=0, column=0, sticky="w")
        
        slider = ttk.Scale(frame, from_=from_, to=to, orient=tk.HORIZONTAL, command=slider_cmd)
        slider.grid(row=0, column=1, sticky="ew", padx=10)
        
        entry = ttk.Entry(frame, textvariable=var, width=7, font=("Helvetica", 10, "bold"), justify='center')
        entry.grid(row=0, column=2, sticky="e")
        entry.bind("<Return>", entry_cmd)
        entry.bind("<FocusOut>", entry_cmd)
        
        return slider, entry

    def _on_temp_slider(self, val):
        if self._updating_from_entry: return
        self._updating_from_slider = True
        self.temp_var.set(f"{float(val):.1f}")
        self.update_plots()
        self._updating_from_slider = False

    def _on_presion_slider(self, val):
        if self._updating_from_entry: return
        self._updating_from_slider = True
        self.presion_var.set(f"{float(val):.1f}")
        self.update_plots()
        self._updating_from_slider = False

    def _on_temp_entry(self, event=None):
        if self._updating_from_slider: return
        self._updating_from_entry = True
        try:
            val = float(self.temp_var.get())
            val = max(0.0, min(120.0, val))
            self.temp_slider.set(val)
            self.temp_var.set(f"{val:.1f}")
            self.update_plots()
        except (ValueError, TclError):
            self.temp_var.set(f"{self.temp_slider.get():.1f}")
        self._updating_from_entry = False

    def _on_presion_entry(self, event=None):
        if self._updating_from_slider: return
        self._updating_from_entry = True
        try:
            val = float(self.presion_var.get())
            val = max(0.0, min(100.0, val))
            self.presion_slider.set(val)
            self.presion_var.set(f"{val:.1f}")
            self.update_plots()
        except (ValueError, TclError):
            self.presion_var.set(f"{self.presion_slider.get():.1f}")
        self._updating_from_entry = False

    def on_closing(self):
        plt.close('all')
        self.root.destroy()
        try:
            os._exit(0)
        except:
            pass

    def update_plots(self):
        temp_val = float(self.temp_slider.get())
        presion_val = float(self.presion_slider.get())

        self.simulacion.input['temperatura_motor'] = temp_val
        self.simulacion.input['presion_aceite'] = presion_val

        try:
            self.simulacion.compute()
            resultado = float(self.simulacion.output['accion_mecanico'])
        except Exception:
            resultado = 0.0

        if resultado <= 40:
            diagnostico = "Revisión de Rutina"
            diag_color = "#28a745"
        elif resultado <= 70:
            diagnostico = "Precaución, revisar pronto"
            diag_color = "#fd7e14"
        else:
            diagnostico = "¡Atención Inmediata!"
            diag_color = "#dc3545"
        
        self.result_value_label.config(text=f"Valor de Urgencia: {resultado:.2f}")
        self.result_text_label.config(text=diagnostico, foreground=diag_color)

        for ax in [self.ax_temp, self.ax_presion, self.ax_accion]:
            ax.clear()
            ax.set_facecolor('#ffffff')
            ax.set_ylim(0, 1.1)

        self.ax_temp.set_xlim(0, 120)
        for term_name, term in self.temperatura_motor.terms.items():
            self.ax_temp.plot(self.temperatura_motor.universe, term.mf, label=term_name)
        self.ax_temp.axvline(x=temp_val, color='r', linestyle='--')
        self.ax_temp.set_title('Temperatura del Motor (°C)')
        self.ax_temp.legend()

        self.ax_presion.set_xlim(0, 100)
        for term_name, term in self.presion_aceite.terms.items():
            self.ax_presion.plot(self.presion_aceite.universe, term.mf, label=term_name)
        self.ax_presion.axvline(x=presion_val, color='r', linestyle='--')
        self.ax_presion.set_title('Presión de Aceite (PSI)')
        self.ax_presion.legend()
        
        self.ax_accion.set_xlim(0, 100)
        for term_name, term in self.accion_mecanico.terms.items():
            self.ax_accion.plot(self.accion_mecanico.universe, term.mf, label=term_name)
        try:
            ups_universe, aggregated, _ = self.accion_mecanico.find_memberships()
            self.ax_accion.fill_between(ups_universe, 0, aggregated, facecolor='indigo', alpha=0.4)
        except Exception: pass
        self.ax_accion.axvline(x=resultado, color='r', linestyle='--')
        self.ax_accion.set_title('Acción del Mecánico')
        self.ax_accion.legend()

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyAutoSystem(root)
    root.mainloop()
