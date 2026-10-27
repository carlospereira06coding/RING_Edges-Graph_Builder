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
 
def three_letter(aa_class: str) -> str:

    aa_dict= {
        "A":"ALA",
        "C":"CYS",
        "D":"ASP",
        "E":"GLU",
        "F":"PHE",
        "G":"GLY",
        "H":"HIS",
        "I":"ILE",
        "K":"LYS",
        "L":"LEU",
        "M":"MET",
        "N":"ASN",
        "P":"PRO",
        "Q":"GLN",
        "R":"ARG",
        "S":"SER",
        "T":"THR",
        "V":"VAL",
        "W":"TRP",
        "Y":"TYR",
    }

    if isinstance(aa_class, str):
        aa = aa_dict.get(aa_class)

    return str(aa)

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
 
def select_aminoacid(data:pd.DataFrame, aa:str) -> pd.DataFrame:
    #Create a list for Pair index, converting ONE-letter --> THREE-letter
    aa_list = [list(aa.strip()) for aa in aa.split(",")]
    #test_list = [three_letter(item[0]) + "".join(item[1:]) for item in aa_list]
    test_list = ["".join(item[1:]) + three_letter(item[0]) for item in aa_list]
    pattern_list = "|".join(test_list)

    print("PATTERN_LIST: ", pattern_list, "\t")
    data = data.drop(columns="Pair")
    """if "Pair" in data.columns:
        filtered_df = data[data["Pair"].str.contains(pat=pattern_list, regex=True, na=False)]
    """
    #Pair is index
    print(data.index)
    mask = data.index.str.contains(pat=pattern_list, regex=True, na=False)
    result = pd.DataFrame(data.loc[mask])
    result.sort_index(inplace=True)
    #print("FILTERED_DF: ", filtered_df)
    return result

"""
Claude added the functions _flatten and _min_max. 

"""



def select_interval(data: pd.DataFrame, domains:list[str]) -> pd.DataFrame: 

    #Separate intervals into int variables
    # Separates 45-219 into integers 45,219
    limits=[]
    for domain in domains:
        lower, top = map(int, re.split(r'[-:,]', domain)) 
        limits.append([lower, top])

    data["Pair"] = [
        [int(i) for i in re.findall(r"\d+",str(label))] for label in data.index
    ]

    mask = pd.Series(False,index=data.index)
    for lower,top in limits:#[[100,219],[515,900]]
        print("LOWER",lower, "\n", "TOP", top, "\n")
        #any(): nenhum dos intervalos satisfaz ambos os dominios. Têm de satisfazer apenas os respetivos. 
        range_mask = data["Pair"].apply(lambda lst: any(lower <= x <= top for x in lst))
        mask |= range_mask
    
    data=pd.DataFrame(data[mask])
    data=data.drop(columns="Pair")
    if len(data)==0:
        print("No interaction pair is contained in both domains")
        return pd.DataFrame()
    return data
