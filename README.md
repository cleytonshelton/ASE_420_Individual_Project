## PLC Code Generator (ASE 420 Individual Project)

Generate ladder-logic text for common conveyor fault sections via a simple GUI. The generator outputs sections for PE Jam, Motor Faults, Comm Faults, Disc Faults, and E-Stop Faults based on your inputs.

---

### ✨ Features
- OOP generator with `Conveyor` and pluggable sections
- Tkinter/ttk GUI for quick generation and file export
- Regression, unit, integration, and acceptance tests

### 🧭 Project Structure
- `generator.py`: OOP code generator and public `generate_plc_code` API
- `gui.py`: Tkinter/ttk GUI app
- `tests/`: pytest suite

### 📦 Requirements
- Python 3.10+
- pip (for installing dev dependencies like pytest)

### 🚀 Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

### 🖥️ Usage (GUI)
```bash
python gui.py
```
1) Enter Conveyor Name, Number of Conveyors, and whether there is a Makeup Unit.
2) Choose a file path with Browse.
3) Click "Generate Code". The status bar shows where the file was saved.

### 🧩 Usage (Library)
```python
from generator import generate_plc_code

code = generate_plc_code("LINE", 3, True)
print(code)
```

### ✅ Testing
Run all tests:
```bash
pytest -q
```
Run subsets:
```bash
pytest -q -k generator
pytest -q -k integration
pytest -q -k acceptance
```

### 📝 Notes
- `MISC_REGS` base index starts at 30 (see `MotorFaultSection`).
- E-Stop lettered zones generated for A–G.

### 🗺 Roadmap
- Configurable parameters (indices, zones) via GUI
- Multiple conveyor type profiles (subclass `Conveyor`)
- Export formats beyond plain text

