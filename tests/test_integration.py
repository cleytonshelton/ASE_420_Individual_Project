import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from generator import generate_plc_code  # noqa: E402


def test_integration_full_string_contains_all_sections():
    code = generate_plc_code("LINE", 3, True)

    titles = [
        "**** PE JAM FAULTS ****",
        "**** MOTOR FAULTS ****",
        "**** COMM FAULTS ****",
        "**** DISC FAULTS ****",
        "**** ESTOP FAULTS ****",
    ]
    for title in titles:
        assert code.count(title) == 1

    # Basic invariants
    for i in range(3):
        assert f"PE_JAM_TMR[{i}]" in code

    expected_misc = [30, 31, 32, 33, 34]
    for idx in expected_misc:
        assert f"MISC_REGS[{idx}]" in code

    assert "_M1_VFD" in code and "_M2_VFD" in code


