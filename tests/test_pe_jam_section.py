import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from generator import Context, PeJamSection


def test_pe_jam_section_basic():
    ctx = Context("LINE", 2, False)
    section = PeJamSection()
    output = section.render(ctx)

    assert output.name == "PE_Jam_Faults"

    # TIMER array size
    assert "PE_JAM_TMR : TIMER[2]" in output.tags[0]

    # Tags for conveyors
    assert any("F_LINE_01_PE_JAM" in t for t in output.tags)
    assert any("F_LINE_02_PE_JAM" in t for t in output.tags)

    # Logic contains rung structure
    assert "LINE-01 PE JAM FAULT" in output.logic
    assert "LINE-02 PE JAM FAULT" in output.logic

    # PE JAM timers present
    assert "PE_JAM_TMR[0]" in output.logic
    assert "PE_JAM_TMR[1]" in output.logic
