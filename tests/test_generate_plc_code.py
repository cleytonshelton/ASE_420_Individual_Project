from generator import Conveyor

def test_generate_code_contains_all_sections():
    code = Conveyor.generate_plc_code_full("LINE", 2, True, "TEST_CTRL")

    # Check the routine names exactly as generated
    assert "ROUTINE PE_Jam_Faults" in code
    assert "ROUTINE Motor_Faults" in code
    assert "ROUTINE Disc_Faults" in code
    assert "ROUTINE EStop_Faults" in code

    # Check MainRoutine calls
    for r in ["PE_Jam_Faults", "Motor_Faults", "Disc_Faults", "EStop_Faults"]:
        assert f"JSR({r},0);" in code

    # Conveyors present
    assert "LINE_01" in code
    assert "LINE_02" in code

    # Makeup unit motors
    assert "LINE_M1_VFD" in code
    assert "LINE_M2_VFD" in code

    # EPBs
    for letter in "ABCDEFG":
        assert f"LINE{letter}_EPB" in code



def test_generate_code_no_mu():
    code = Conveyor.generate_plc_code_full("LINE", 2, False, "TEST_CTRL")

    # MU motors should not appear
    assert "LINE_M1_VFD" not in code
    assert "LINE_M2_VFD" not in code

    # MISC registers should only account for conveyors
    assert "MISC_REGS[30]" in code  # conveyor 1
    assert "MISC_REGS[31]" in code  # conveyor 2
    assert "MISC_REGS[32]" not in code  # MU M1
    assert "MISC_REGS[33]" not in code  # MU M2
