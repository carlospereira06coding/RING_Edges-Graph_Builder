import config
from config import *
from graph import *
from compare import *
import pandas as pd
from freq_build import *
import filter

def backup_files():

    pass
    
if __name__ == "__main__":


    """
    compare.py

    file_build(): filename, data, index --> Create output.csv files
    select_interval() --> Print all interactions in a specific domain or between two or more domains.
    build_table() --> Restructure the data into "ResNum, Amino_Acid, Interaction columns"
    """

    T = BUILD_TABLE()
    T.build_table(
        interval_check=False,
        paths_dict=config.dict_path,
        build_csv=True
    )


    """
    Freq_build.py
    """

    F_CONTROL = FREQ_TABLE(T)
    F_AA = FREQ_TABLE(T)

    df_control = F_CONTROL.bond_freq_calc(columns=F_CONTROL.CONTROL_columns, build_csv=True)
    df_aa = F_AA.bond_freq_calc(columns=F_AA.AA_columns, build_csv=True)


    if isinstance(df_control, pd.DataFrame) and isinstance(df_aa, pd.DataFrame):
        df_control = filter.select_interval(data=df_control, domain_1=DOMAIN_1, domain_2=DOMAIN_2)
        df_aa = filter.select_interval(data=df_aa, domain_1=DOMAIN_1, domain_2=DOMAIN_2)

    """
    Graph.py : building the frequency files 
    """

    #Select domain interval, multiple amino acids, select "inter" or "intra" domain interactions.


    CONTROL_TITLE = f"{config.CONTROL_TITLE}_{config.DOMAIN_1}_{config.DOMAIN_2}"
    AA_TITLE = f"{config.AA_TITLE}_{config.DOMAIN_1}_{config.DOMAIN_2}"
    
    fig1, axes = butterfly(
        df_left=df_control,
        df_right=df_aa,
        left_title=str(CONTROL_TITLE),
        right_title=str(AA_TITLE),
        figsize=(9,20)
    )

    fig1.savefig(Path(output_dir)/f"{CONTROL_TITLE}-{AA_TITLE}.png", dpi=150)
    

