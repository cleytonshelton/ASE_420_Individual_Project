import string
from tkinter import ttk
from generator import generate_plc_code
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()
root.title("PLC Code Generator")
root.geometry("480x360")
root.resizable(False, False)

# Theming
try:
    style = ttk.Style()
    if 'vista' in style.theme_names():
        style.theme_use('vista')
    elif 'clam' in style.theme_names():
        style.theme_use('clam')
except Exception:
    pass

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Main frame
main = ttk.Frame(root, padding=(16, 16, 16, 12))
main.grid(row=0, column=0, sticky="nsew")
main.columnconfigure(0, weight=1)

title_label = ttk.Label(main, text="PLC Code Generator", font=("Segoe UI", 12, "bold"))
title_label.grid(row=0, column=0, pady=(0, 12), sticky="w")

# Form frame
form = ttk.LabelFrame(main, text="Inputs", padding=(12, 10, 12, 10))
form.grid(row=1, column=0, sticky="nsew")
form.columnconfigure(0, weight=0)
form.columnconfigure(1, weight=1)
form.columnconfigure(2, weight=0)

# Conveyor Name label, input field, and variable
ttk.Label(form, text="Conveyor Name:").grid(row=0, column=0, padx=(0, 8), pady=6, sticky="e")
conv_name_var = tk.StringVar()
conv_name_entry = ttk.Entry(form, width=28, textvariable=conv_name_var)
conv_name_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=6)

# Number of Conveyors label, input field, and variable
ttk.Label(form, text="Number of Conveyors:").grid(row=1, column=0, padx=(0, 8), pady=6, sticky="e")
num_of_conv_var = tk.StringVar()
num_of_conv_entry = ttk.Entry(form, width=28, textvariable=num_of_conv_var)
num_of_conv_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=6)

# Checkbox for a Makeup Unit
is_MU_var = tk.BooleanVar()
is_MU_check = ttk.Checkbutton(form, text="Does this line have a Makeup Unit?", variable=is_MU_var)
is_MU_check.grid(row=2, column=1, columnspan=2, pady=6, sticky="w")

# Filepath label, input field, and variable
ttk.Label(form, text="Filepath to write code into:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=6)
filepath_var = tk.StringVar()
filepath_entry = ttk.Entry(form, width=28, textvariable=filepath_var)
filepath_entry.grid(row=3, column=1, pady=6, sticky="ew")

# Browse button to open file explorer with a default of a .txt file
def browse_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if file_path:
        filepath_var.set(file_path)

browse_button = ttk.Button(form, text="📂 Browse...", command=browse_file)
browse_button.grid(row=3, column=2, sticky="w", padx=(8, 0), pady=6)

# Function to save user input and print to console
def save_input():
    conv_name = conv_name_var.get()
    num_of_conv = num_of_conv_var.get()
    is_MU = is_MU_var.get()
    filepath = filepath_var.get()

    try:
        num = int(num_of_conv)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter an integer")

    if not conv_name or not num_of_conv or not filepath:
        messagebox.showerror("Missing Information", "Please fill in all the text fields.")
        return

    try:
        code = generate_plc_code(conv_name, num, is_MU)
        with open(filepath, 'w') as file:
            file.write(code)
    except Exception as e:
        messagebox.showerror("File Error", f"An error occurred while writing to the file: {e}")
        return
            
    status_var.set(f"Saved to: {filepath}")

    conv_name_var.set("")
    num_of_conv_var.set("")
    is_MU_var.set(False)
    filepath_var.set("")
    
save_button = ttk.Button(main, text="⚙️ Generate Code", command=save_input)
save_button.grid(row=2, column=0, pady=(12, 6), sticky="e")

# Status bar (empty by default, smaller font when showing saved path)
status_var = tk.StringVar(value="")
status = ttk.Label(root, textvariable=status_var, anchor="w", font=("Segoe UI", 8))
status.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))

# Start the main event loop
root.mainloop()