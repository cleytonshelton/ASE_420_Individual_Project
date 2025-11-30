# PLC Code Generator - User Manual

## Overview

The **PLC Code Generator** is a desktop application that generates RSLogix/Studio 5000 L5K PLC code for conveyor systems. Users can specify the conveyor line, number of conveyors, makeup units, and output file location. The tool automatically creates routines and global tags for PE Jam, Motor Faults, Disc Faults, and E-Stop Faults.

---

## System Requirements

- Windows 10 or higher
- Python 3.10+ installed
- Tkinter library (comes with Python)
- Access to Studio 5000 or RSLogix 5000 to import `.L5K` files

---

## Installation

1. Clone or download the project repository.
2. Ensure Python is installed and added to your system PATH.
3. (Optional) Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/Scripts/activate  # Windows
    ```

4. Install required dependencies (if any):

    ```bash
    pip install -r requirements.txt
    ```

5. Run the application:

    ```bash
    python gui.py
    ```

---

## User Interface

### Main Window

- **Controller Name**: Name of the PLC controller.
- **Conveyor Name**: Identifier for the conveyor line (e.g., `LineA`).
- **Number of Conveyors**: Total number of conveyors in the line.
- **Makeup Unit**: Checkbox to indicate if the line has a makeup unit.
- **Filepath**: Path where the generated `.L5K` file will be saved.
- **Browse...**: Opens a file dialog to choose the save location.
- **Generate Code**: Button to generate the PLC code.

### Status Bar

- Displays messages such as:
  - ✅ `Saved to: [filepath]` on success
  - ❌ Error messages if input is invalid

---

## How to Use

1. Open the application:

    ```bash
    python gui.py
    ```

2. Fill in the required fields:
    - Controller Name
    - Conveyor Name
    - Number of Conveyors
    - Select Makeup Unit if applicable
    - Filepath to save the `.L5K` file

3. Click **Generate Code**.
4. Check the **status bar** for success confirmation.
5. Open the generated `.L5K` file in Studio 5000 for import.

---

## Input Validation

- **All fields are required**. Leaving any field empty will display an error.
- **Number of Conveyors** must be an integer. Invalid entries will display an error.
- Output file path must be writable.

---

## Notes

- Generated PLC code includes:
  - **PE Jam Faults**
  - **Motor Faults**
  - **Disc Faults**
  - **E-Stop Faults**
- File is UTF-8 encoded and ready to import into Studio 5000.

---

## Troubleshooting

- **Tkinter Errors**: Ensure Python was installed with Tkinter support.
- **Permission Denied**: Ensure the save path is writable.
- **Invalid Input**: Check that all fields are filled correctly and the number of conveyors is numeric.
