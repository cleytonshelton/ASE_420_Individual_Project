import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from generator import Context, MotorFaultSection


def test_motor_faults_no_mu():
    ctx = Context("LINE", 2, False)
    sec = MotorFaultSection()
    out = sec.render(ctx)

    assert out.name == "Motor_Faults"

    # Make sure MU motors are not created
    assert not any("_M1_VFD" in line for line in out.logic)
    assert not any("_M2_VFD" in line for line in out.logic)

    # Ensure misc regs increment correctly
    assert "MISC_REGS[30]" in out.logic
    assert "MISC_REGS[31]" in out.logic


def test_motor_faults_with_mu():
    ctx = Context("LINE", 1, True)
    sec = MotorFaultSection()
    out = sec.render(ctx)

    # MU motors (M1, M2) should exist
    assert "_M1_VFD" in out.logic
    assert "_M2_VFD" in out.logic

    # MISC registers should include base + conveyors + MU motors
    assert "MISC_REGS[30]" in out.logic  # conveyor
    assert "MISC_REGS[31]" in out.logic  # MU M1
    assert "MISC_REGS[32]" in out.logic  # MU M2
