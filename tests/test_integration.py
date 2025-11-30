import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from generator import Conveyor


def test_integration_full_string_contains_all_sections():
    # Call new generator with 4 arguments
    code = Conveyor.generate_plc_code_full("LINE", 3, True, "TEST_CTRL")

    # Check that all routines are present in the generated code
    routine_names = [
        "PE_Jam_Faults",
        "Motor_Faults",
        "Disc_Faults",
        "EStop_Faults",
    ]
    for name in routine_names:
        assert f"ROUTINE {name}" in code

    # Check MainRoutine calls all routines
    for name in routine_names:
        assert f"JSR({name},0);" in code

    # Check per-conveyor PE_JAM_TMR
    for i in range(3):
        assert f"PE_JAM_TMR[{i}]" in code

    # Check misc registers from MotorFaultSection
    expected_misc = [30, 31, 32, 33, 34]  # indices as per your generator logic
    for idx in expected_misc:
        assert f"MISC_REGS[{idx}]" in code

    # Makeup unit motors
    assert "_M1_VFD" in code and "_M2_VFD" in code
