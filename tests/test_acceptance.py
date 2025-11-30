import sys
import os
from pathlib import Path
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generator import Conveyor  # <-- import the class, not a function

def test_acceptance_writes_file_and_has_expected_lines(tmp_path: Path):
    tmp_dir = tmp_path / "out"
    tmp_dir.mkdir()
    out_file = tmp_dir / "gen.txt"

    # Call the static method
    code = Conveyor.generate_plc_code_full("ACPT", 2, True, "TEST_CTRL")
    out_file.write_text(code, encoding="utf-8")

    assert out_file.exists() and out_file.stat().st_size > 0

    text = out_file.read_text(encoding="utf-8")
    assert "PE_Jam_Faults" in text
    assert "EStop_Faults" in text
    assert "ACPT_01" in text and "ACPT_02" in text
    assert "ACPT_M1_VFD" in text and "ACPT_M2_VFD" in text


@pytest.mark.parametrize(
    "num,has_mu,expected_misc_last",
    [
        (1, False, 30),
        (2, False, 31),
        (1, True, 32),
    ],
)
def test_misc_regs_progression(num, has_mu, expected_misc_last):
    code = Conveyor.generate_plc_code_full("MISC", num, has_mu, "TEST_CTRL")
    assert f"MISC_REGS[{expected_misc_last}]" in code
