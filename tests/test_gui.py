import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add project root to path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import after adjusting sys.path
from gui import PLCCodeGeneratorApp

# ------------------------
# Fixtures
# ------------------------
@pytest.fixture
def app():
    """Return a fresh instance of the app with Tkinter mocked."""
    with patch("tkinter.Tk", autospec=True):
        app_instance = PLCCodeGeneratorApp.__new__(PLCCodeGeneratorApp)
        # Manually initialize variables without calling Tk.__init__
        app_instance.status_var = MagicMock()
        app_instance.cont_name_var = MagicMock()
        app_instance.conv_name_var = MagicMock()
        app_instance.num_of_conv_var = MagicMock()
        app_instance.is_MU_var = MagicMock()
        app_instance.filepath_var = MagicMock()
        yield app_instance

# ------------------------
# Tests
# ------------------------
def test_missing_fields_shows_error(app):
    """Check error is shown if any required field is empty."""
    app.cont_name_var.get.return_value = ""
    app.conv_name_var.get.return_value = "LineA"
    app.num_of_conv_var.get.return_value = "2"
    app.filepath_var.get.return_value = "C:/temp/test.L5K"

    with patch("tkinter.messagebox.showerror") as mock_error:
        app.save_input()
        mock_error.assert_called_once_with(
            "Missing Information",
            "Please fill in all the text fields."
        )

def test_invalid_number_input_shows_error(app):
    """Check error is shown if number of conveyors is not an integer."""
    app.cont_name_var.get.return_value = "CTRL1"
    app.conv_name_var.get.return_value = "LineA"
    app.num_of_conv_var.get.return_value = "invalid"
    app.filepath_var.get.return_value = "C:/temp/test.L5K"

    with patch("tkinter.messagebox.showerror") as mock_error:
        app.save_input()
        mock_error.assert_called_once_with(
            "Invalid Input",
            "Number of Conveyors must be an integer."
        )

def test_successful_save_resets_fields(app):
    """Check that after successful save, fields are reset and status updated."""
    app.cont_name_var.get.return_value = "CTRL1"
    app.conv_name_var.get.return_value = "LineA"
    app.num_of_conv_var.get.return_value = "2"
    app.is_MU_var.get.return_value = True
    app.filepath_var.get.return_value = "C:/temp/test.L5K"

    # Mock the Conveyor.generate_plc_code_full to avoid real file generation
    with patch("generator.Conveyor.generate_plc_code_full", return_value="PLC_CODE"), \
         patch("builtins.open", create=True) as mock_open:
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        app.save_input()

        # Verify file write
        mock_file.write.assert_called_once_with("PLC_CODE")

        # Check fields reset
        app.cont_name_var.set.assert_called_with("")
        app.conv_name_var.set.assert_called_with("")
        app.num_of_conv_var.set.assert_called_with("")
        app.is_MU_var.set.assert_called_with(False)
        app.filepath_var.set.assert_called_with("")

def test_status_updated_on_success(app):
    """Ensure status_var is updated with success message."""
    app.cont_name_var.get.return_value = "CTRL1"
    app.conv_name_var.get.return_value = "LineA"
    app.num_of_conv_var.get.return_value = "1"
    app.is_MU_var.get.return_value = False
    app.filepath_var.get.return_value = "C:/temp/test.L5K"

    with patch("generator.Conveyor.generate_plc_code_full", return_value="PLC_CODE"), \
         patch("builtins.open", create=True):
        app.save_input()
        app.status_var.set.assert_called_once()
        # Check that the filepath appears in the success message
        assert "C:/temp/test.L5K" in app.status_var.set.call_args[0][0]
