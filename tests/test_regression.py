import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from generator import generate_plc_code  # Your new refactored code

# ----- Old code reproduced as a function for regression testing -----
def old_generate_code(conv_name: str, num: int, is_MU: bool) -> str:
    """Simulates the output of the old code (all rungs on one line, title on newline)."""
    import string

    output = f"**** PE JAM FAULTS **** \n"
    # PE JAM FAULTS
    rungs = []
    for i in range(1, num + 1):
        rungs.append(
            f"[XIO(I_{conv_name}_{i:02}_PE_HEAD_END)[XIC({conv_name}_{i:02}_VFD:I.Data[0].4),XIC(E3D_READ[0].{i-1})]"
            f"[TON(PE_JAM_TMR[{i-1}],?,?),XIC(PE_JAM_TMR[{i-1}].DN)OTL(F_{conv_name}_{i:02}_PE_JAM)],"
            f"XIC(I_{conv_name}_{i:02}_PE_HEAD_END)XIC(F_{conv_name}_{i:02}_PE_JAM)XIC(F_CS_{conv_name}_{i:02}_EPB)"
            f"XIO(I_CS_{conv_name}_{i:02}_EPB)XIC(I_CS_{conv_name}_{i:02}_SPB)OTU(F_{conv_name}_{i:02}_PE_JAM)];"
        )
    output += "".join(rungs)

    # MOTOR FAULTS
    output += "\n**** MOTOR FAULTS **** \n"
    misc_index = 30
    rungs = []
    for i in range(1, num + 1):
        rungs.append(
            f"[[XIC({conv_name}_{i:02}_VFD:O.Data[0].7)XIO({conv_name}_{i:02}_VFD:I.Data[0].4),"
            f"XIO({conv_name}_{i:02}_VFD:O.Data[0].7)XIC({conv_name}_{i:02}_VFD:I.Data[0].4)]"
            f"TON({conv_name}_{i:02}_VFD_FAULTED_FAULT_TMR,?,?),"
            f"XIC(I_MCP_DC01_EZONE1_ESCR)[XIC({conv_name}_{i:02}_VFD_FAULTED_FAULT_TMR.DN),"
            f"XIO(F_{conv_name}_{i:02}_VFD_COMM_FLT)XIC({conv_name}_{i:02}_VFD:I.Data[0].8)ONS(MISC_REGS[{misc_index}].0)]"
            f"OTL(F_{conv_name}_{i:02}_VFD_FLT)];"
        )
        misc_index += 1

    if is_MU:
        for i in range(1, 3):
            rungs.append(
                f"[[XIC({conv_name}_M{i}_VFD:O.Data[0].7)XIO({conv_name}_M{i}_VFD:I.Data[0].4),"
                f"XIO({conv_name}_M{i}_VFD:O.Data[0].7)XIC({conv_name}_M{i}_VFD:I.Data[0].4)]"
                f"TON({conv_name}_M{i}_VFD_FAULTED_FAULT_TMR,?,?),"
                f"XIC(I_MCP_{conv_name}_EZONE3_ESCR)[XIC({conv_name}_M{i}_VFD_FAULTED_FAULT_TMR.DN),"
                f"XIO(F_{conv_name}_M{i}_VFD_COMM_FLT)XIC({conv_name}_M{i}_VFD:I.Data[0].8)ONS(MISC_REGS[{misc_index}].0)]"
                f"OTL(F_{conv_name}_M{i}_VFD_FLT)];"
            )
            misc_index += 1

    output += "".join(rungs)

    # COMM FAULTS
    output += "\n**** COMM FAULTS **** \n"
    rungs = []
    for i in range(1, num + 1):
        rungs.append(f"XIC({conv_name}_{i:02}_VFD:I.ConnectionFaulted)OTE(F_{conv_name}_{i:02}_VFD_COMM_FLT);")
    if is_MU:
        for i in range(1, 3):
            rungs.append(f"XIC({conv_name}_M{i}_VFD:I.ConnectionFaulted)OTE(F_{conv_name}_M{i}_VFD_COMM_FLT);")
    output += "".join(rungs)

    # DISC FAULTS
    output += "\n**** DISC FAULTS **** \n"
    rungs = []
    for i in range(1, num + 1):
        rungs.append(f"XIO(I_{conv_name}_{i:02}_MSD)OTE(F_{conv_name}_{i:02}_MSD);")
    if is_MU:
        for i in range(1, 3):
            rungs.append(f"XIO(I_{conv_name}_M{i}_MSD)OTE(F_{conv_name}_M{i}_MSD);")
    output += "".join(rungs)

    # ESTOP FAULTS
    output += "\n**** ESTOP FAULTS **** \n"
    rungs = []
    for i in range(1, num + 1):
        rungs.append(f"[XIC(I_CS_{conv_name}_{i:02}_EPB)OTL(F_CS_{conv_name}_{i:02}_EPB),"
                     f"XIO(I_CS_{conv_name}_{i:02}_EPB)XIC(I_CS_{conv_name}_{i:02}_SPB)OTU(F_CS_{conv_name}_{i:02}_EPB)];")
    for letter in string.ascii_uppercase[:7]:
        rungs.append(f"[XIC(I_CS_{conv_name}{letter}_EPB)OTL(F_CS_{conv_name}{letter}_EPB),"
                     f"XIO(I_CS_{conv_name}{letter}_EPB)XIC(I_CS_{conv_name}{letter}_KSW)OTU(F_CS_{conv_name}{letter}_EPB)];")
    output += "".join(rungs)

    return output

# ----- Regression tests -----
@pytest.mark.parametrize(
    "conv_name,num,is_MU",
    [
        ("LINE", 2, False),
        ("LINE", 1, True),
        ("CONV", 3, True),
    ]
)
def test_regression(conv_name, num, is_MU):
    old_code = old_generate_code(conv_name, num, is_MU)
    new_code = generate_plc_code(conv_name, num, is_MU)
    assert new_code == old_code, "Refactored code does not match original code output"
