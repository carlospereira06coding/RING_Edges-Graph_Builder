from config import *
from graph import *
from compare import *
import pandas as pd
from freq_build import *
import filter
import logging
import json


BAR_HEIGHT = 0.6

def sort_idx(df):
    def natural_key(idx: pd.Index) -> pd.Index: 
        return idx.str.extract(r"(\d+)", expand=False).astype(int) #As type int converte as str numericas em objetos int, permitindo ordenação numérica.

    ordered = df.sort_index(key=natural_key, inplace=False)
    print(ordered)
    return ordered
    
def box_interval(data:pd.DataFrame, domains:list[str]):
    
    #Extracts the chunk of domain being rendered in butterfly: '14ARG' --> '14' --> 14
    pairs = [
        [int(i) for i in re.findall(r"\d+", str(label))] for label in data.index
    ]

    #For each domain searched (DOMAIN_TITLE), the loop converts "domain" list[str] into int
    for domain, DOMAIN_TITLE in zip(domains, DOMAIN_CONFIG.keys()):
        lower, top = map(int, re.findall(r"\d+", str(domain)))
        mask = np.array(
            [lower <= pair[0] <= top for pair in pairs]
        )
        rows=np.where(mask)[0] #Select all
        DOMAIN_CONFIG[DOMAIN_TITLE]["rows"] = [int(rows.min()), int(rows.max())] if rows.size else None


def butterfly_fig_render(DF_LEFT:pd.DataFrame, DF_RIGHT:pd.DataFrame, DOMAINS:list[str]=[], SEARCH_SEQUENCE:list[str]=[], figsize=(9,20), dpi=150, path:str=""):

    TITLES = DOMAINS if len(DOMAINS)!=0 else SEARCH_SEQUENCE 
    parts = [str(p) for p in TITLES if p]
    left_title = "_".join([str(config.CONTROL_TITLE), *parts])
    right_title = "_".join([str(config.AA_TITLE), *parts])
    #stem = f"{left_title}_{right_title}"
    stem = "_".join(parts)

    img_output = output_dir/path/f"{stem}"
    img_output.mkdir(parents=True, exist_ok=True) #Se o path output das imagens ainda não existir, não cria um novo diretório.

    #Garante que uma coluna temporaria "Pair" não pode entrar no dataframe de frequências.
    DF_LEFT = DF_LEFT.drop(columns="Pair", errors="ignore")
    DF_RIGHT = DF_RIGHT.drop(columns="Pair", errors="ignore")


    chunk_size=HBAR_CONFIG["CHUNK_SIZE"]
    font=float(np.clip(0.22*72*0.55, 6, 12))
    plt.rcParams.update(
        {
            "axes.labelsize":font*1.2,
            "xtick.labelsize": font,
            "ytick.labelsize": font,
            "figure.dpi": 150,
        }
    )

    
    df_chunks=[]
    max_total=0
    for i in range(0, max(len(DF_LEFT), len(DF_RIGHT)), chunk_size):
        chunk_right = pd.DataFrame(DF_RIGHT.iloc[i:i+chunk_size, :])
        chunk_left = pd.DataFrame(DF_LEFT.iloc[i:i+chunk_size, :])
        #print("DF_RIGHT", chunk_right.index)
        #print("DF_LEFT", chunk_left.index)
        df_chunks.append((chunk_right, chunk_left))

    for idx, (df_l, df_r) in enumerate(df_chunks, start=1):
        
        nrows = max(len(df_l), len(df_r))
        if len(DOMAINS)!=0:
            box_interval(data=df_l, domains=DOMAINS)

    
        fig, (ax_left, ax_right) = butterfly(
            df_left=df_l,
            df_right=df_r,
            left_title=left_title,
            right_title=right_title,
            max_total=max_total
        )

        print(f"DOMAIN_CONFIG_{idx}", DOMAIN_CONFIG.items(), "\n")
        for DOMAIN_TITLE, cfg in DOMAIN_CONFIG.items():
            
            rows, color = cfg["rows"], cfg["color"]
            print("LINE:", rows, color)

            if rows is None: continue
            YMIN = min(nrows, rows[0])
            YMAX = min(nrows, rows[1])

            if DOMAIN_CONFIG[DOMAIN_TITLE] != [0,0]:
                
                ax_left.axhspan(
                    ymin=YMIN,
                    ymax=YMAX,
                    facecolor=color,
                    alpha=0.1,
                    zorder=1
                )

                ax_right.axhspan(
                    ymin=YMIN,
                    ymax=YMAX,
                    facecolor=color,
                    alpha=0.1,
                    zorder=1
                )

                ax_left.plot(
                    [HBAR_CONFIG["POS_X"], HBAR_CONFIG["POS_X"]],
                    [YMIN, YMAX],
                    linewidth=2.5,
                    transform=ax_left.get_yaxis_transform(),
                    clip_on=False,
                    color=color
                )

                ax_left.text(
                    x=HBAR_CONFIG["POS_X"]-0.1,
                    y=(YMIN+YMAX)/2,
                    s=DOMAIN_TITLE,
                    fontsize=15,
                    ha="center",
                    va="center",
                    color=color,
                    transform=ax_left.get_yaxis_transform(),
                    clip_on=False,
                    rotation=90
                )


        handles, labels = ax_right.get_legend_handles_labels()
        ax_pos = ax_right.get_position()
        fig.legend(
            handles=handles,
            labels=labels,
            fontsize=font,
            loc='lower center',
            borderaxespad=2,
            ncol=len(labels),
            bbox_to_anchor=[0.57, -(ax_pos.y0 - 0.07)]
        )
        save_path = img_output/ f"img_{idx}.png"
        fig.savefig(str(save_path), dpi=150, bbox_inches='tight', pad_inches=0.3)
        plt.close(fig)
    
if __name__ == "__main__":


    """
    compare.py

    file_build(): filename, data, index --> Create output.csv files
    select_interval() --> Print all interactions in a specific domain or between two or more domains.
    build_table() --> Restructure the data into "ResNum, Amino_Acid, Interaction columns"
    """
    
    """
    Build the log file
    """
    
    logging.basicConfig(filename="RING_log_config.log", filemode="w")

    paths_dict:dict[str, tuple[list[Path],list[str]]] = config.dict_path
    control_tuple = paths_dict.get("CONTROL", ([], [])) #Empty lists garantees a obbject != None if the key isnt found in the dictionary.
    test_tuple = paths_dict.get("TEST", ([], []))

    control_paths, CONTROL_columns = control_tuple
    test_paths, AA_columns = test_tuple

    T = BUILD_TABLE()
    T.build_table(
        pathlist=control_paths+test_paths,
    )

    """
    Freq_build.py
    """

    sort_idx(T.ct_data).to_csv(output_dir/"full-compare-table", sep=";", index=True)

    F = FREQ_TABLE(T)
    print("CONTROL:", CONTROL_columns, "\n", "AA:", AA_columns)
    df_control = sort_idx(F.bond_freq_calc(columns=CONTROL_columns))
    df_aa = sort_idx(F.bond_freq_calc(columns=AA_columns))

    df_control.to_csv(path_or_buf=output_dir/f"{CONTROL_TITLE}_bond-freq", sep=";", index=True)
    df_aa.to_csv(path_or_buf=output_dir/f"{AA_TITLE}_bond-freq", sep=";", index=True)

    """
    Design a check that choses the non-empty dataframe as the reference for row central categorical values and if both are empty, 
    no image will be produced. If met, the non-empty dataframe should be used to create an image, 
    where the left just mirrors that categories in the non-empty dataframe but keeps it empty. 
    
    """

    df_control_single = sort_idx(F.single_aa_freq_calc(df=df_control))
    df_aa_single = sort_idx(F.single_aa_freq_calc(df=df_aa))

    df_control_single.to_csv(path_or_buf=output_dir/f"{CONTROL_TITLE}_single-freq", sep=";", index=True)
    df_aa_single.to_csv(path_or_buf=output_dir/f"{AA_TITLE}_single-freq", sep=";", index=True)

    if isinstance(df_control, pd.DataFrame) and isinstance(df_aa, pd.DataFrame) and isinstance(df_control_single, pd.DataFrame) and isinstance(df_aa_single, pd.DataFrame):
        domain_1 = DOMAINS[0]
        domain_2 = DOMAINS[1]

        DOMAIN_1_TITLE = "CINASE"
        DOMAIN_2_TITLE = "TPR"
        DOMAIN_CONFIG = {
            DOMAIN_1_TITLE: {"rows":None, "color" : "#1F7210"}, 
            DOMAIN_2_TITLE: {"rows":None, "color": "#C57020"}
        }

        #print("DOMAIN_1:",domain_1, "\n", "DOMAIN_2:", domain_2)
        df_control_interval = filter.select_interval(data=df_control, domains=DOMAINS)
        df_aa_interval = filter.select_interval(data=df_aa, domains=DOMAINS)
        df_control_single_interval = filter.select_interval(data=df_control_single, domains=DOMAINS)
        df_aa_single_interval = filter.select_interval(data=df_aa_single, domains=DOMAINS)
        """print("DF_AA:",df_aa)
        print("DF_AA_SINGLE:", df_aa_single)
        print("DF_AA_INTERVAL:", df_aa_interval)
        print("DF_CONTROL:", df_control)
        print("DF_CONTROL_SINGLE:", df_control_single)
        print("DF_CONTROL_INTERVAL:", df_control_interval)"""
        butterfly_fig_render(DF_LEFT=df_control_interval, DF_RIGHT=df_aa_interval, DOMAINS=DOMAINS, path="INTERACTIONS")
        butterfly_fig_render(DF_LEFT=df_control_single_interval, DF_RIGHT=df_aa_single_interval, DOMAINS=DOMAINS)

        if SEARCH_SEQUENCE!=None:
            df_control_sel_aa = filter.select_aminoacid(data=df_control, aa=SEARCH_SEQUENCE)
            df_aa_sel_aa = filter.select_aminoacid(data=df_aa, aa=SEARCH_SEQUENCE)
            butterfly_fig_render(DF_LEFT=df_control_sel_aa, DF_RIGHT=df_aa_sel_aa, SEARCH_SEQUENCE=[SEARCH_SEQUENCE], figsize=(10,10))
