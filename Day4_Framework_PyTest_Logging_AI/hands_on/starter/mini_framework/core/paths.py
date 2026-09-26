"""Central place for folder paths - no other module hard-codes a path."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
TEST_DATA_DIR = ROOT / "test_data"
LOG_DIR = ROOT / "logs"
REPORT_DIR = ROOT / "reports"
SCREENSHOT_DIR = ROOT / "screenshots"
