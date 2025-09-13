import tkinter as tk
from tkinter import filedialog

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

tk.Label(root, text="Conveyor Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
conv_name_var = tk.StringVar()
conv_name_entry = tk.Entry(root, width=30, textvariable=conv_name_var)
conv_name_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

tk.Label(root, text="Number of Conveyors:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
num_of_conv_var = tk.StringVar()
num_of_conv_entry = tk.Entry(root, width=30, textvariable=num_of_conv_var)
num_of_conv_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)

is_MU_var = tk.BooleanVar()
is_MU_check = tk.Checkbutton(root, text="Does this line have a Makeup Unit?", variable=is_MU_var)
is_MU_check.grid(row=3, column=0, columnspan=3, pady=5)

tk.Label(root, text="Filepath to write code into:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
filepath_var = tk.StringVar()
filepath_entry = tk.Entry(root, width=30, textvariable=filepath_var)
filepath_entry.grid(row=4, column=1, pady=5, sticky="w")

def browse_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if file_path:
        filepath_var.set(file_path)

browse_button = tk.Button(root, text="Browse...", command=browse_file)
browse_button.grid(row=4, column=2, sticky="s", padx=5, pady=5)

def save_input():
    conv_name = conv_name_var.get()
    num_of_conv = num_of_conv_var.get()
    is_MU = is_MU_var.get()
    print(f"User input: {conv_name}")
    print(f"Number of conveyors: {num_of_conv}")
    print(f"Does this have a MU? {is_MU}")

save_button = tk.Button(root, text="Generate Code", command=save_input)
save_button.grid(row=5, column=0, columnspan=3, pady=20)

# Start the main event loop
root.mainloop()