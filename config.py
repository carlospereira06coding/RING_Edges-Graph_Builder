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

now= datetime.now().strftime("%y%m%d_%H-%M-%S")
datetime.now().strftime("%d-%m-%y_%H-%M")

#LOAD personal environment file for this run
load_dotenv(dotenv_path=os.environ["dir_name"])

output_dir = Path(str(os.getenv('OUTPUT_DIR'))) / f"{os.getenv('CONTROL_TITLE')}-{os.getenv('AA_TITLE')}"

if output_dir.exists():
    base = output_dir
    i = 1
    while (candidate := Path(f"{base}_{i}")).exists():
        i += 1
    output_dir = candidate

output_dir.mkdir(parents=True, exist_ok=True)


#LOAD selected files' paths 
control_string = os.getenv("CONTROL_RING_PATH")
aa_string = os.getenv("AA_ring_path")

if not control_string or not aa_string:
    raise ValueError("The variables werent defined in the .env file")#aa_string, control_string are str|None. This if-statement garantees that the variable read is always str.

CONTROL_dir_list = [f for f in Path(control_string).iterdir()]
AA_dir_list = [f for f in Path(aa_string).iterdir()]

"""
dict_path's values are in tuple format.
(Pathlist, file names)

"""

dict_path = {
    'CONTROL' : (CONTROL_dir_list, [p.stem for p in CONTROL_dir_list]),
    'TEST' : (AA_dir_list, [p.stem for p in AA_dir_list])
}

DOMAIN_1 = str(os.getenv('DOMAIN_1'))
DOMAIN_2 = str(os.getenv('DOMAIN_2'))

CONTROL_TITLE = os.getenv("CONTROL_TITLE") 
AA_TITLE = os.getenv("AA_TITLE")