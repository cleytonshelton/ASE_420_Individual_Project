import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class PLCCodeGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PLC Code Generator")
        self.geometry("500x360")
        self.resizable(False, False)
        self._apply_theme()
        self._build_ui()

    def _apply_theme(self):
        style = ttk.Style()
        for theme in ('vista', 'clam', 'default'):
            if theme in style.theme_names():
                style.theme_use(theme)
                break

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.status_var = tk.StringVar(value="")

        main = ttk.Frame(self, padding=(16, 16))
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)

        ttk.Label(main, text="PLC Code Generator", font=("Segoe UI", 14, "bold"))\
            .grid(row=0, column=0, sticky="w", pady=(0, 12))

        self._build_form(main)

        # Generate Code button
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=2, column=0, sticky="e", pady=(12, 0))
        ttk.Button(btn_frame, text="⚙️ Generate Code", command=self.save_input).pack()

        # Status label
        ttk.Label(self, textvariable=self.status_var, anchor="w", font=("Segoe UI", 8))\
            .grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))

    def _build_form(self, parent):
        form = ttk.LabelFrame(parent, text="Inputs", padding=(12, 10))
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(1, weight=1)  # Make entry column expand

        # Variables
        self.conv_name_var = tk.StringVar()
        self.num_of_conv_var = tk.StringVar()
        self.is_MU_var = tk.BooleanVar()
        self.filepath_var = tk.StringVar()

        # Conveyor Name
        ttk.Label(form, text="Conveyor Name:").grid(row=0, column=0, padx=(0, 8), pady=6, sticky="e")
        ttk.Entry(form, textvariable=self.conv_name_var).grid(row=0, column=1, columnspan=2, sticky="ew", pady=6)

        # Number of Conveyors
        ttk.Label(form, text="Number of Conveyors:").grid(row=1, column=0, padx=(0, 8), pady=6, sticky="e")
        ttk.Entry(form, textvariable=self.num_of_conv_var).grid(row=1, column=1, columnspan=2, sticky="ew", pady=6)

        # Makeup Unit Checkbox
        ttk.Checkbutton(form, text="Does this line have a Makeup Unit?", variable=self.is_MU_var)\
            .grid(row=2, column=1, columnspan=2, sticky="w", pady=6)

        # Filepath
        ttk.Label(form, text="Filepath to write code into:").grid(row=3, column=0, padx=(0, 8), pady=6, sticky="e")
        ttk.Entry(form, textvariable=self.filepath_var).grid(row=3, column=1, sticky="ew", pady=6)
        ttk.Button(form, text="📂 Browse...", command=self.browse_file).grid(row=3, column=2, padx=(8,0), pady=6, sticky="w")

    def browse_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.filepath_var.set(file_path)

    def save_input(self):
        conv_name = self.conv_name_var.get().strip()
        num_of_conv = self.num_of_conv_var.get().strip()
        is_MU = self.is_MU_var.get()
        filepath = self.filepath_var.get().strip()

        if not conv_name or not num_of_conv or not filepath:
            messagebox.showerror("Missing Information", "Please fill in all the text fields.")
            return

        try:
            num = int(num_of_conv)
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of Conveyors must be an integer.")
            return

        try:
            from generator import generate_plc_code
            code = generate_plc_code(conv_name, num, is_MU)
            with open(filepath, 'w') as file:
                file.write(code)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return

        self.status_var.set(f"✅ Saved to: {filepath}")
        self.conv_name_var.set("")
        self.num_of_conv_var.set("")
        self.is_MU_var.set(False)
        self.filepath_var.set("")


if __name__ == "__main__":
    app = PLCCodeGeneratorApp()
    app.mainloop()
