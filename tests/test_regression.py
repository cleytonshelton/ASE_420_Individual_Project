import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from generator import Conveyor

import string

def old_rung_variables(conv_name: str, num: int, is_MU: bool):
    """Return the list of expected variable substrings from the old code"""
    vars = []

    # PE JAM
    for i in range(1, num + 1):
        vars.append(f"F_{conv_name}_{i:02}_PE_JAM")
        vars.append(f"PE_JAM_TMR[{i-1}]")
    # MOTOR FAULTS
    misc_index = 30
    for i in range(1, num + 1):
        vars.append(f"F_{conv_name}_{i:02}_VFD_FLT")
        vars.append(f"MISC_REGS[{misc_index}]")
        misc_index += 1
    if is_MU:
        for i in range(1, 3):
            vars.append(f"F_{conv_name}_M{i}_VFD_FLT")
            vars.append(f"MISC_REGS[{misc_index}]")
            misc_index += 1
    # COMM
    for i in range(1, num + 1):
        vars.append(f"F_{conv_name}_{i:02}_VFD_COMM_FLT")
    if is_MU:
        for i in range(1, 3):
            vars.append(f"F_{conv_name}_M{i}_VFD_COMM_FLT")
    # DISC
    for i in range(1, num + 1):
        vars.append(f"F_{conv_name}_{i:02}_MSD")
    if is_MU:
        for i in range(1, 3):
            vars.append(f"F_{conv_name}_M{i}_MSD")
    # ESTOP
    for i in range(1, num + 1):
        vars.append(f"F_CS_{conv_name}_{i:02}_EPB")
    for letter in string.ascii_uppercase[:7]:
        vars.append(f"F_CS_{conv_name}{letter}_EPB")
    return vars


@pytest.mark.parametrize(
    "conv_name,num,is_MU",
    [
        ("LINE", 2, False),
        ("LINE", 1, True),
        ("CONV", 3, True),
    ]
)
def test_regression(conv_name, num, is_MU):
    new_code = Conveyor.generate_plc_code_full(conv_name, num, is_MU, "TEST_CTRL")

    # Check all expected variables/rungs exist in new code
    expected_vars = old_rung_variables(conv_name, num, is_MU)
    for var in expected_vars:
        assert var in new_code, f"Expected variable/rung {var} missing in new code"

    # Optionally, check that MainRoutine calls all routines
    routine_names = [
        "PE_Jam_Faults",
        "Motor_Faults",
        "Disc_Faults",
        "EStop_Faults",
    ]
    for name in routine_names:
        assert f"JSR({name},0);" in new_code
