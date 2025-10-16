import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from generator import (
    generate_plc_code,
    Context,
    PeJamSection,
    MotorFaultSection,
    CommFaultSection,
    DiscFaultSection,
    EStopFaultSection,
)


@pytest.fixture
def basic_context():
    # Simple test context with 2 conveyors and no makeup unit
    return Context(conveyor_name="LINE", num_conveyors=2, has_makeup_unit=False)


def test_pe_jam_section(basic_context):
    section = PeJamSection()
    code = section.render(basic_context)

    # Check the title line appears
    assert "**** PE JAM FAULTS ****" in code
    # Check correct number of conveyors generated
    assert code.count("PE_JAM_TMR") == basic_context.num_conveyors * 2
    # Check variable names are formatted correctly
    assert "LINE_01" in code and "LINE_02" in code


def test_motor_fault_section_without_makeup(basic_context):
    section = MotorFaultSection()
    code = section.render(basic_context)

    assert "**** MOTOR FAULTS ****" in code
    # No makeup unit motors expected
    assert "_M1_VFD" not in code
    # Check misc index increments
    assert "MISC_REGS[30]" in code and "MISC_REGS[31]" in code


def test_motor_fault_section_with_makeup():
    ctx = Context("LINE", 1, True)
    section = MotorFaultSection()
    code = section.render(ctx)

    assert "_M1_VFD" in code
    assert "_M2_VFD" in code


def test_comm_fault_section(basic_context):
    section = CommFaultSection()
    code = section.render(basic_context)

    assert "**** COMM FAULTS ****" in code
    assert "F_LINE_01_VFD_COMM_FLT" in code
    assert "F_LINE_02_VFD_COMM_FLT" in code


def test_disc_fault_section_with_makeup():
    ctx = Context("LINE", 1, True)
    section = DiscFaultSection()
    code = section.render(ctx)

    assert "**** DISC FAULTS ****" in code
    assert "LINE_M1_MSD" in code
    assert "LINE_M2_MSD" in code


def test_estop_fault_section(basic_context):
    section = EStopFaultSection()
    code = section.render(basic_context)

    assert "**** ESTOP FAULTS ****" in code
    # Check one of each EPB type
    assert "LINE_01" in code
    assert "LINE_02" in code
    # Lettered EPBs
    for letter in "ABCDEFG":
        assert f"LINE{letter}_EPB" in code


def test_generate_plc_code_full():
    code = generate_plc_code("LINE", 2, True)
    # Ensure all section titles are in the generated string
    for title in [
        "**** PE JAM FAULTS ****",
        "**** MOTOR FAULTS ****",
        "**** COMM FAULTS ****",
        "**** DISC FAULTS ****",
        "**** ESTOP FAULTS ****",
    ]:
        assert title in code
