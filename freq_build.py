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

    def unpack_row(self, row):
        
        models = [model for model in row._fields if model != "Index"]
        """
        O que é uma nova interação? Procuramos todas as interações diferentes registadas na linha.
        """

        row_freq={}
        for model in models:
            BOND=getattr(row, model)
            if isinstance(BOND, str):
                interactions=BOND.split()
                for inter in interactions:
                    row_freq[inter]=1

        return row_freq
    

    def single_aa_freq_calc(self, df:pd.DataFrame):

        """
            Build frequency table not for interaction pairs, 
            but for single amino acids.
        
        """

        def transform(name:pd.Index)->pd.Index:
            return name.map(lambda a: a.split(":")[0])

        freq_df = df.groupby(by=transform(df.index)).sum()
        return freq_df


    
    def bond_freq_calc(self, columns)->pd.DataFrame:

        def row_parser(dict:dict):
            for bond in list(dict.keys()):
                curr_value = dict.get(bond)
                new_name = str(bond.split(":")[0])
                if dict.get(new_name) != None:
                    dict[new_name] += curr_value
                    del dict[bond]
                else:
                    dict[new_name] = dict.pop(bond)

        
        df = self.ct_data
        #print("CT_DATA: ", self.ct_data.iloc[:3])
        self.bond_freq = pd.DataFrame(
            columns=["HBOND", "IONIC", "PICATION", "PIPISTACK", "VDW"], 
        )

        self.bond_freq.index.name = "Pair"

        print("FREQ_BUILD (INDEX)", df.index.names)
        print("FREQ_BUILD (COLUMNS)", df.columns)
        print("SELECTED columns: ", columns)

        for row in df[columns].itertuples(index=True):
            row_freq = self.unpack_row(row=row)
            row_parser(dict=row_freq)
            self.bond_freq.loc[row.Index] = pd.Series(row_freq)

        self.bond_freq.fillna(value=0, inplace=True)
                    
        return self.bond_freq
