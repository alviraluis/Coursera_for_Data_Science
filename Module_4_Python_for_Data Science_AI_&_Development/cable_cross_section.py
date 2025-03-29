import math
import tkinter as tk
from tkinter import ttk, messagebox

# Calculate current based on power, voltage, power factor, and phase type
def calculate_current(power, voltage, power_factor, phase_type):
    if phase_type == 'single':
        current = power / (voltage * power_factor)
    elif phase_type == 'three':
        current = power / (math.sqrt(3) * voltage * power_factor)
    else:
        raise ValueError("phase_type must be either 'single' or 'three'")
    return current

# Adjust current using correction factors k1 and k2
def apply_correction_factors(current, k1, k2):
    return current / (k1 * k2)

# Select cable cross-section based on calculated current and conductor material
# Values are simplified according to ABB and IEC standards
def select_cross_section(current, conductor_material):
    cross_section_table_cu = [
        (1.5, 18), (2.5, 24), (4, 32), (6, 41), (10, 57),
        (16, 76), (25, 101), (35, 125), (50, 151), (70, 192),
        (95, 232), (120, 269), (150, 300), (185, 341), (240, 400)
    ]

    cross_section_table_al = [
        (16, 61), (25, 80), (35, 99), (50, 119), (70, 150),
        (95, 179), (120, 207), (150, 230), (185, 263), (240, 308)
    ]

    table = cross_section_table_cu if conductor_material == 'copper' else cross_section_table_al

    for size, ampacity in table:
        if current <= ampacity:
            return size

    raise ValueError("Current too high for standard cable sizes.")

# Calculate voltage drop and percentage voltage drop
def voltage_drop(length, current, voltage, cross_section, conductor_material, phase_type, power_factor):
    resistivity = {'copper': 0.0178, 'aluminum': 0.029}
    R = resistivity[conductor_material] * length / cross_section

    if phase_type == 'single':
        v_drop = 2 * current * R * power_factor
    else:  # three-phase
        v_drop = math.sqrt(3) * current * R * power_factor

    percent_v_drop = (v_drop / voltage) * 100

    return v_drop, percent_v_drop

# GUI application
def run_gui():
    def calculate():
        try:
            voltage = float(voltage_entry.get())
            power = float(power_entry.get())
            power_factor = float(power_factor_entry.get())
            phase_type = phase_var.get()
            k1 = float(k1_entry.get())
            k2 = float(k2_entry.get())
            conductor_material = conductor_var.get()
            insulator_material = insulator_var.get()
            length = float(length_entry.get())

            current = calculate_current(power, voltage, power_factor, phase_type)
            corrected_current = apply_correction_factors(current, k1, k2)
            cross_section = select_cross_section(corrected_current, conductor_material)
            v_drop, percent_v_drop = voltage_drop(length, current, voltage, cross_section, conductor_material, phase_type, power_factor)

            result = (
                f"Calculated current: {current:.2f} A\n"
                f"Corrected current (with k1, k2): {corrected_current:.2f} A\n"
                f"Recommended cable cross-section: {cross_section} mm² ({conductor_material.title()}/{insulator_material})\n"
                f"Voltage drop: {v_drop:.2f} V ({percent_v_drop:.2f}%)"
            )

            messagebox.showinfo("Calculation Results", result)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}\nPlease check your inputs and try again.")

    root = tk.Tk()
    root.title("Cable Sizing Calculator")

    ttk.Label(root, text="Voltage (V):").grid(row=0, column=0)
    voltage_entry = ttk.Entry(root)
    voltage_entry.grid(row=0, column=1)

    ttk.Label(root, text="Power (W):").grid(row=1, column=0)
    power_entry = ttk.Entry(root)
    power_entry.grid(row=1, column=1)

    ttk.Label(root, text="Power Factor:").grid(row=2, column=0)
    power_factor_entry = ttk.Entry(root)
    power_factor_entry.grid(row=2, column=1)

    ttk.Label(root, text="Phase Type:").grid(row=3, column=0)
    phase_var = tk.StringVar(value="three")
    ttk.OptionMenu(root, phase_var, "three", "single", "three").grid(row=3, column=1)

    ttk.Label(root, text="Correction Factor k1:").grid(row=4, column=0)
    k1_entry = ttk.Entry(root)
    k1_entry.grid(row=4, column=1)

    ttk.Label(root, text="Correction Factor k2:").grid(row=5, column=0)
    k2_entry = ttk.Entry(root)
    k2_entry.grid(row=5, column=1)

    ttk.Label(root, text="Conductor Material:").grid(row=6, column=0)
    conductor_var = tk.StringVar(value="copper")
    ttk.OptionMenu(root, conductor_var, "copper", "copper", "aluminum").grid(row=6, column=1)

    ttk.Label(root, text="Insulator Material:").grid(row=7, column=0)
    insulator_var = tk.StringVar(value="PVC")
    ttk.OptionMenu(root, insulator_var, "PVC", "PVC", "XLPE").grid(row=7, column=1)

    ttk.Label(root, text="Cable Length (m):").grid(row=8, column=0)
    length_entry = ttk.Entry(root)
    length_entry.grid(row=8, column=1)

    ttk.Button(root, text="Calculate", command=calculate).grid(row=9, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
