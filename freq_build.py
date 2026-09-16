from config import *
from compare import BUILD_TABLE


class FREQ_TABLE(BUILD_TABLE):

    #INHERITANCE METHODS/ ATRIBUTES
    def __init__(self, build_table_object:BUILD_TABLE):
        """
        self.ct_data : file created from pd.DataFrame(), processed in compare.build_table()
        self.bond_type : Dictionary holds 2 different chemical bond frequency dataframes, separating between control and test group
        """
        super().__init__()

        # Copy all attributes populated in instance 'T' onto 'self'
        self.__dict__.update(build_table_object.__dict__)

        #self.bond_type: dict[str, pd.DataFrame]
        self.bond_freq= pd.DataFrame()
        self.group_freq= pd.DataFrame()

    def cell_split(self, cell:str)->int:
        #Separate HBOND:MC_MC VDW:MC_SC --> ["HBOND:MC_MC","VDW:MC_SC"] = 2
        try: 
            if isinstance(cell,str) and cell.strip():
                lst=cell.split()
                return len(lst)
            return 0
        except:
            return 0 #if cell is NaN: 0


    def aa_freq_calc(self):
            """
            Build frequency table not for interaction pairs, 
            but for single amino acids.
            """
            pass

    """def select_interval(self, domain_1:str, domain_2:str)-> pd.DataFrame: 
        #Separate intervals into 
        lower_d1, top_d1 = map(int, re.split(r'[-:,]', domain_1)) # Separates 45-219 into integers 45,219
        lower_d2, top_d2 = map(int, re.split(r'[-:,]', domain_2))

        df = self.ct_data
        # Separate ResNum column into 2 integer columns
        print("FILTER: ", list(df.columns), list(df.index.names))

        res_split = df.loc["Pair"].str.split(":", expand=True).astype(int) # Separation of ResNum column into 2 integer columns
        res_1: pd.Series[int] = res_split[0]
        res_2: pd.Series[int] = res_split[1]

        #Selecting rows through vectorized filtering
        mask = (
        (res_1 >= lower_d1) & (res_1 <= top_d1)
        & (res_2 >= lower_d2) & (res_2 <= top_d2)
        )

        return df[mask]"""
    
    def bond_freq_calc(self, columns, build_csv:bool, grouped=False)->pd.DataFrame:

        def _strip_bond(value):
                if pd.isna(value):
                    return np.nan
                return str(value).split(":")[0]

        split_df = self.ct_data[["ResNum","Amino Acid"]].apply(lambda col: col.str.split(":"))
        
        pair_index = (split_df["Amino Acid"].str[0]) + (split_df["ResNum"].str[0]) + ":" + (split_df["Amino Acid"].str[1]) + (split_df["ResNum"].str[1])

        df = (
            self.ct_data[columns].assign(Pair=pair_index).set_index("Pair")
        )

        for col in columns:# COLUMNS is the interval we are searching (CONTROL or TEST)
            #Change column values, ignoring SC/MC. "HBOND"--> ttk_human_model_0_HBOND
            df[col] = df[col].map(_strip_bond)

        #df.to_csv(path_or_buf=Path(".").resolve().parent/"BITCH.csv", sep=";")

        #One Hot Encode columns except index "Pair". 
        dummy_encoded = pd.get_dummies(df, columns=columns, dtype='int')

        #dummy_encoded.to_csv(path_or_buf=Path(".").resolve().parent/"DUMMY.csv",sep=";")


        """
        val in df[col].unique(): unique value in current dataframe column;
        val for col in df.columns: iterate through each column in dataframe

        """
        unique_bond = {str(val) for col in df.columns for val in df[col].unique() if pd.notna(val)}
        
        """

        #Sum frequency for each type of bond type: count of models with that bond in that interaction pair
        bond_freq_data = {
            bond: dummy_encoded[[c for c in dummy_encoded.columns if c.endswith(f"_{bond}")]].sum(axis=1)
            for bond in unique_bond
        }
        self.bond_freq = pd.DataFrame(bond_freq_data, index=dummy_encoded.index)
        """

        lookup_dict = {}

        for col in dummy_encoded.columns:
            suff = col.split("_")[-1]  # Splits column name string and extracts suffix
            if suff in lookup_dict:
                lookup_dict[suff].append(col)
            else:
                lookup_dict[suff]=[col]


        bond_freq_data = {
            bond: dummy_encoded[[col for col in lookup_dict[bond]]].sum(axis=1) for bond in unique_bond
        }


        self.bond_freq = pd.DataFrame(bond_freq_data, index=dummy_encoded.index)
        #self.bond_freq.to_csv(path_or_buf=Path(".").resolve().parent/"BOND_FREQ_F.csv", sep=";")

        self.bond_freq.to_csv(path_or_buf=Path(".").resolve().parent/"bond_model_freq.csv", sep=";", index=True)

        if grouped:
            self.group_freq = pd.DataFrame(self.bond_freq.sum(axis=1))
            if build_csv:
                self.bond_freq.to_csv(path_or_buf=Path(output_dir)/"grouped_model_freq.csv", sep=";", index=False)

        if build_csv:
            #self.bond_freq.to_csv(path_or_buf=Path(output_dir)/"bond_model_freq.csv", sep=";", index=True)
            pass
        return self.bond_freq
