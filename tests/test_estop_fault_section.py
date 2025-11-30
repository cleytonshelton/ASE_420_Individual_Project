import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from generator import Context, EStopFaultSection


def test_estop_fault_section():
    ctx = Context("LINE", 2, False)
    sec = EStopFaultSection()
    out = sec.render(ctx)

    assert out.name == "EStop_Faults"

    # Base MCP tags
    assert any("I_MCP_LINE_EPB" in t for t in out.tags)
    assert any("F_MCP_LINE_EPB" in t for t in out.tags)

    # Per-conveyor EPBs
    assert any("F_CS_LINE_01_EPB" in t for t in out.tags)
    assert any("F_CS_LINE_02_EPB" in t for t in out.tags)

    # Logic contains latch/unlatch rungs
    assert "OTL(F_CS_LINE_01_EPB)" in out.logic
    assert "OTU(F_CS_LINE_01_EPB)" in out.logic

    # A–G letter EPBs must exist
    for letter in "ABCDEFG":
        assert any(f"I_CS_LINE{letter}_EPB" in t for t in out.tags)
