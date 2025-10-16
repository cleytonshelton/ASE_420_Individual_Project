import os
import sys
from pathlib import Path
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from generator import generate_plc_code  # noqa: E402


def test_acceptance_writes_file_and_has_expected_lines(tmp_path: Path):
    tmp_dir = tmp_path / "out"
    tmp_dir.mkdir()
    out_file = tmp_dir / "gen.txt"

    code = generate_plc_code("ACPT", 2, True)
    out_file.write_text(code, encoding="utf-8")

    assert out_file.exists() and out_file.stat().st_size > 0

    text = out_file.read_text(encoding="utf-8")
    assert "**** PE JAM FAULTS ****" in text
    assert "**** ESTOP FAULTS ****" in text
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
    code = generate_plc_code("MISC", num, has_mu)
    assert f"MISC_REGS[{expected_misc_last}]" in code


