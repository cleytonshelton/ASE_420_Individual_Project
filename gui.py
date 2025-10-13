import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Create the main window
root = tk.Tk()

# Set window title
root.title("PLC Code Generator")

# Set window size
root.geometry("450x350")
root.resizable(False, False)  # Prevent resizing for simplicity

# Add a label to the window
label = tk.Label(root, text="PLC Code Generator")
label.grid(row=0, column=0, columnspan=3, pady=(15, 10)) # Add some padding for better appearance

# Conveyor Name label, input field, and variable
tk.Label(root, text="Conveyor Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
conv_name_var = tk.StringVar()
conv_name_entry = tk.Entry(root, width=30, textvariable=conv_name_var)
conv_name_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

# Number of Conveyors label, input field, and variable
tk.Label(root, text="Number of Conveyors:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
num_of_conv_var = tk.StringVar()
num_of_conv_entry = tk.Entry(root, width=30, textvariable=num_of_conv_var)
num_of_conv_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)

# Checkbox for a Makeup Unit
is_MU_var = tk.BooleanVar()
is_MU_check = tk.Checkbutton(root, text="Does this line have a Makeup Unit?", variable=is_MU_var)
is_MU_check.grid(row=3, column=0, columnspan=3, pady=5)

# Filepath label, input field, and variable
tk.Label(root, text="Filepath to write code into:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
filepath_var = tk.StringVar()
filepath_entry = tk.Entry(root, width=30, textvariable=filepath_var)
filepath_entry.grid(row=4, column=1, pady=5, sticky="w")

# Browse button to open file explorer with a default of a .txt file
def browse_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if file_path:
        filepath_var.set(file_path)

browse_button = tk.Button(root, text="Browse...", command=browse_file)
browse_button.grid(row=4, column=2, sticky="s", padx=5, pady=5)

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
        with open(filepath, 'w') as file:
            # PE JAM FAULTS
            file.write("**** PE JAM FAULTS **** \n")
            for i in range(1, num + 1):
               file.write(f"[XIO(I_{conv_name}_{i:02}_PE_HEAD_END)[XIC({conv_name}_{i:02}_VFD:I.Data[0].4),XIC(E3D_READ[0].{i-1})][TON(PE_JAM_TMR[{i-1}],?,?),XIC(PE_JAM_TMR[{i-1}].DN)OTL(F_{conv_name}_{i:02}_PE_JAM)],XIC(I_{conv_name}_{i:02}_PE_HEAD_END)XIC(F_{conv_name}_{i:02}_PE_JAM)XIC(F_CS_{conv_name}_{i:02}_EPB)XIO(I_CS_{conv_name}_{i:02}_EPB)XIC(I_CS_{conv_name}_{i:02}_SPB)OTU(F_{conv_name}_{i:02}_PE_JAM)];")

            # MOTOR FAULTS
            file.write("\n**** MOTOR FAULTS **** \n")
            # MISC_REGS index starting point (placeholder change for each project)
            j = 30
            for i in range(1, num + 1):
                file.write(f"[[XIC({conv_name}_{i:02}_VFD:O.Data[0].7)XIO({conv_name}_{i:02}_VFD:I.Data[0].4),XIO({conv_name}_{i:02}_VFD:O.Data[0].7)XIC({conv_name}_{i:02}_VFD:I.Data[0].4)]TON({conv_name}_{i:02}_VFD_FAULTED_FAULT_TMR,?,?),XIC(I_MCP_DC01_EZONE1_ESCR)[XIC({conv_name}_{i:02}_VFD_FAULTED_FAULT_TMR.DN),XIO(F_{conv_name}_{i:02}_VFD_COMM_FLT)XIC({conv_name}_{i:02}_VFD:I.Data[0].8)ONS(MISC_REGS[{j}].0)]OTL(F_{conv_name}_{i:02}_VFD_FLT)];")
                j = j + 1

            # COMM FAULTS
            file.write("\n**** COMM FAULTS **** \n")
            for i in range(1, num + 1):
                file.write(f"XIC({conv_name}_{i:02}_VFD:I.ConnectionFaulted)OTE(F_{conv_name}_{i:02}_VFD_COMM_FLT);")
            
            # DISC FAULTS
            file.write("\n**** DISC FAULTS ****")
            for i in range(1, num + 1):
                file.write(f"XIO(I_{conv_name}_{i:02}_MSD)OTE(F_{conv_name}_{i:02}_MSD);")
    except Exception as e:
        messagebox.showerror("File Error", f"An error occurred while writing to the file: {e}")
        return
            
    print(f"User input: {conv_name}")
    print(f"Number of conveyors: {num_of_conv}")
    print(f"Does this have a MU? {is_MU}")
    print(f"Filepath: {filepath}")

    conv_name_var.set("")
    num_of_conv_var.set("")
    is_MU_var.set(False)
    filepath_var.set("")
    
save_button = tk.Button(root, text="Generate Code", command=save_input)
save_button.grid(row=5, column=0, columnspan=3, pady=20)

# Start the main event loop
root.mainloop()