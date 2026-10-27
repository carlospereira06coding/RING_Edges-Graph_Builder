import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from datetime import datetime
import re
from typing import overload
from dotenv import load_dotenv
import logging
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Any
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator


"""
Function import_env_var(): Retrieves every exported environment variable 
loaded into memory from the bash script by .sh script

"""

logger = logging.getLogger(__name__)

# Load .env if there is one. load_dotenv() returns False (no error) when no file is found,
# but we wrap it anyway so a malformed or unreadable file can't crash the import either.
try:
    ENV_FILE_FOUND = load_dotenv()
except Exception as e:
    logger.warning("Could not load .env file: %s", e)
    ENV_FILE_FOUND = False

if not ENV_FILE_FOUND:
    logger.warning("No .env file loaded; falling back to existing environment variables only.")


def import_env_var(var, required=False) -> str | None:
    """Retrieve an environment variable. Returns None if missing (logs a warning if required)."""
    value = os.getenv(var)
    if not value:
        if required:
            logger.warning(f"Required variable {var} isn't defined (no .env file or variable not set)")
        return None
    return value


BASH_TIME = os.getenv("BASH_TIME", "")

OUTPUT_DIR = import_env_var("OUTPUT_DIR", required=True)
CONTROL_RING_PATH = import_env_var("CONTROL_RING_PATH", required=True)
AA_RING_PATH = import_env_var("AA_RING_PATH", required=True)
CONTROL_TITLE = import_env_var("CONTROL_TITLE", required=True)
AA_TITLE = import_env_var("AA_TITLE", required=True)

# Optional parameters
SEARCH_SEQUENCE = import_env_var("SEARCH_SEQUENCE")
DOMAIN_1 = import_env_var("DOMAIN_1")
DOMAIN_2 = import_env_var("DOMAIN_2")
DOMAINS: list[str] = [d for d in (DOMAIN_1, DOMAIN_2) if isinstance(d, str)]

# Only build paths if every required variable is available
CONFIG_COMPLETE = all([OUTPUT_DIR, CONTROL_RING_PATH, AA_RING_PATH, CONTROL_TITLE, AA_TITLE])

HBAR_CONFIG = {
    "YLIM" : [0,0],
    "TITLE_PAD" : 40,
    "LABEL_PAD" : 10,
    "LABEL_FONT_SIZE" : 10,
    "BAR_HEIGHT": 0.8,
    "CHUNK_SIZE":100,
    "POS_X" : -0.125
}


output_dir: Path
CONTROL_dir_list: list[Path] = []
AA_dir_list: list[Path] = []

if CONFIG_COMPLETE:
    try:
        output_dir = Path(str(OUTPUT_DIR)) / BASH_TIME / f"{CONTROL_TITLE}--{AA_TITLE}"
        output_dir.mkdir(parents=True, exist_ok=True)

        CONTROL_dir_list = list(Path(str(CONTROL_RING_PATH)).iterdir())
        AA_dir_list = list(Path(str(AA_RING_PATH)).iterdir())
    except (OSError, ValueError) as e:  # missing folders, permissions, bad paths
        logger.warning("Could not set up paths from environment: %s", e)
else:
    logger.warning("Configuration incomplete; paths were not initialised.")

"""
dict_path's values are in tuple format.
(Pathlist, file names)
"""
dict_path = {
    'CONTROL': (CONTROL_dir_list, [p.stem for p in CONTROL_dir_list]),
    'TEST': (AA_dir_list, [p.stem for p in AA_dir_list]),
}

DOMAIN_1_TITLE="CINASE"
DOMAIN_2_TITLE="TPR"
DOMAIN_CONFIG = {
    DOMAIN_1_TITLE: {"rows":None, "color" : "#1F7210"}, 
    DOMAIN_2_TITLE: {"rows":None, "color": "#C57020"}
}