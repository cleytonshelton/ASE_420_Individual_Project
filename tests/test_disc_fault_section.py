import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from generator import Context, DiscFaultSection


def test_disc_fault_basic_no_mu():
    ctx = Context("LINE", 2, False)
    sec = DiscFaultSection()
    out = sec.render(ctx)

    assert out.name == "Disc_Faults"

    # Per conveyor tags
    assert "F_LINE_01_MSD" in " ".join(out.tags)
    assert "F_LINE_02_MSD" in " ".join(out.tags)

    # Logic contains OTE rungs
    assert "OTE(F_LINE_01_MSD)" in out.logic
    assert "OTE(F_LINE_02_MSD)" in out.logic


def test_disc_fault_with_mu():
    ctx = Context("LINE", 1, True)
    sec = DiscFaultSection()
    out = sec.render(ctx)

    # MU tags
    assert "F_LINE_M1_MSD" in " ".join(out.tags)
    assert "F_LINE_M2_MSD" in " ".join(out.tags)

    # MU logic
    assert "OTE(F_LINE_M1_MSD)" in out.logic
    assert "OTE(F_LINE_M2_MSD)" in out.logic
