import tkinter as tk

# Create the main window
root = tk.Tk()

# Set window title
root.title("PLC Code Generator")

# Set window size
root.geometry("400x300")

# Add a label to the window
label = tk.Label(root, text="PLC Code Generator")
label.pack(pady=20) # Add some padding for better appearance

conv_name_var = tk.StringVar()
num_of_conv_var = tk.StringVar()

conv_name_input_frame = tk.Frame(root)
conv_name_input_frame.pack(pady=10)

conv_name_label = tk.Label(conv_name_input_frame, text="Conveyor Name:")
conv_name_label.pack(side="left", padx=5)

conv_name = tk.Entry(conv_name_input_frame, width=30, textvariable=conv_name_var)
conv_name.pack(side="left", padx=5)

num_of_conv_frame = tk.Frame(root)
num_of_conv_frame.pack(pady=10)

num_of_conv_label = tk.Label(num_of_conv_frame, text="Number of Conveyors:")
num_of_conv_label.pack(side="left", padx=5)

num_of_conv_entry = tk.Entry(num_of_conv_frame, width=30, textvariable=num_of_conv_var)
num_of_conv_entry.pack(side="left", padx=5)

def save_input():
    user_input = conv_name_var.get()
    num_of_conv = num_of_conv_var.get()
    print(f"User input: {user_input}")
    print(f"Number of conveyors: {num_of_conv}")

save_button = tk.Button(root, text="Save Input", command=save_input)
save_button.pack(pady=10)

# Start the main event loop
root.mainloop()