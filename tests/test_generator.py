import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from generator import (
    Conveyor,
    Context,
    PeJamSection,
    MotorFaultSection,
    DiscFaultSection,
    EStopFaultSection,
)


@pytest.fixture
def basic_context():
    return Context(conveyor_name="LINE", num_conveyors=2, has_makeup_unit=False)


def test_pe_jam_section(basic_context):
    section = PeJamSection()
    output = section.render(basic_context)

    # Check RoutineOutput properties
    assert output.name == "PE_Jam_Faults"
    assert len(output.tags) >= basic_context.num_conveyors  # at least one tag per conveyor
    # Check ladder logic contains conveyor names
    for i in range(1, basic_context.num_conveyors + 1):
        assert f"LINE_{i:02}" in output.logic


def test_motor_fault_section_without_makeup(basic_context):
    section = MotorFaultSection()
    output = section.render(basic_context)

    assert output.name == "Motor_Faults"
    # No makeup units
    for m in ["_M1_VFD", "_M2_VFD"]:
        assert m not in output.logic
    # Misc registers start at 30
    assert "MISC_REGS[30]" in output.logic


def test_motor_fault_section_with_makeup():
    ctx = Context("LINE", 1, True)
    section = MotorFaultSection()
    output = section.render(ctx)

    for m in ["_M1_VFD", "_M2_VFD"]:
        assert m in output.logic


def test_disc_fault_section_with_makeup():
    ctx = Context("LINE", 1, True)
    section = DiscFaultSection()
    output = section.render(ctx)

    assert output.name == "Disc_Faults"
    for m in ["LINE_M1_MSD", "LINE_M2_MSD"]:
        assert m in output.logic


def test_estop_fault_section(basic_context):
    section = EStopFaultSection()
    output = section.render(basic_context)

    assert output.name == "EStop_Faults"
    # Check that conveyor numbers and letters are included
    for i in range(1, basic_context.num_conveyors + 1):
        assert f"LINE_{i:02}" in output.logic
    for letter in "ABCDEFG":
        assert f"LINE{letter}_EPB" in output.logic


def test_generate_plc_code_full():
    # Call new generator
    code = Conveyor.generate_plc_code_full("LINE", 2, True, "TEST_CTRL")

    # Ensure routines exist
    for routine_name in ["PE_Jam_Faults", "Motor_Faults", "Disc_Faults", "EStop_Faults"]:
        assert f"ROUTINE {routine_name}" in code

    # Ensure MainRoutine calls them all
    for routine_name in ["PE_Jam_Faults", "Motor_Faults", "Disc_Faults", "EStop_Faults"]:
        assert f"JSR({routine_name},0);" in code
