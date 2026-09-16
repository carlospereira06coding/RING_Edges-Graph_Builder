#pd.DataFrame compatible method
from config import *
from compare import BUILD_TABLE
from freq_build import FREQ_TABLE
import re

def one_letter(aa_class: pd.DataFrame|list[str]) -> pd.DataFrame| pd.Series | list[str|None]:
    aa_dict = {
        "ALA":"A",
        "CYS":"C",
        "ASP":"D",
        "GLU":"E",
        "PHE":"F",
        "GLY":"G",
        "HIS":"H",
        "ILE":"I",
        "LYS":"K",
        "LEU":"L",
        "MET":"M",
        "ASN":"N",
        "PRO":"P",
        "GLN":"Q",
        "ARG":"R",
        "SER":"S",
        "THR":"T",
        "VAL":"V",
        "TRP":"W",
        "TYR":"Y"
    }
    #Create a map and apply it across the axis: Series
    if isinstance(aa_class, pd.Series):
        aa = aa_class.map(aa_dict.get) #lambda function

    elif isinstance(aa_class, pd.DataFrame):
        aa = aa_class.map(lambda x: aa_dict.get(x))

    if isinstance(aa_class, (list)):
        aa = list(map(aa_dict.get, aa_class))

    return aa
 

def RN_AA_code():
    pass

def Pair_code():
    pass

def aa_or_pos_code():
    pass

def exist_in_col():
    pass

"""
SELECT INTERVAL:
In the current version, it's only possible to print info about the interaction of 2 domains.
The available info would be entries in RING files, compare files, frequency tables;
The returned dataframe can be used for graphing methods.

"""

def select_interval(data: pd.DataFrame, domain_1:str, domain_2:str)-> pd.DataFrame: 
    #Separate intervals into 
    lower_d1, top_d1 = map(int, re.split(r'[-:,]', domain_1)) # Separates 45-219 into integers 45,219
    lower_d2, top_d2 = map(int, re.split(r'[-:,]', domain_2))

    df: pd.DataFrame = data

    res_split = df.index.str.split(":", expand=True) # Separation of ResNum column into 2 integer columns

    res_1 = pd.Series(res_split.get_level_values(0).str.extract(r"(\d+)", expand=False), index=df.index).astype(int)
    res_2 = pd.Series(res_split.get_level_values(1).str.extract(r"(\d+)", expand=False), index=df.index).astype(int)

    #Selecting rows through vectorized filtering
    mask = (
    (res_1 >= lower_d1) & (res_1 <= top_d1)
    & (res_2 >= lower_d2) & (res_2 <= top_d2)
    )

    result = (data.loc[mask]).sort_values(by=["Pair"])
    return result