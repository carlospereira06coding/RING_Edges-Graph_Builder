from config import *
import config

class BUILD_TABLE():

    def __init__(self):
        self.ct_data = pd.DataFrame()
        self.CONTROL_columns : list[str]
        self.AA_columns : list[str]
        pass

    def file_build(self, filename:str, data:pd.DataFrame): #Build every dataframe as a csv file 

        try:
            data.to_csv(path_or_buf=Path(output_dir) / f"{filename}.csv", sep=";")
            data.fillna("--").to_html(buf=Path(output_dir) / f"{filename}.html")

        #log created file in run cycle log
        except:
            pass #Log failed attempt

    def select_interval(self, domains:list[list[int]]): 
        """
        Checks all the interactions in a specific domain or between two or more domains 
        """

        pass

    def build_table(self, paths_dict: dict[str, tuple[list[Path],list[str]]], interval_check:bool=False, build_csv:bool=True,**kwargs): #If TRUE, generate a csv file. ELSE save pd in BUILD_TABLE.data

        self.ct_data = pd.DataFrame(columns=["ResNum","Amino Acid"])
        self.ct_data = self.ct_data.set_index("ResNum", drop=False)


        control_tuple = paths_dict.get("CONTROL", ([], [])) #Empty lists garantees a obbject != None if the key isnt found in the dictionary.
        test_tuple = paths_dict.get("TEST", ([], []))

        control_paths, self.CONTROL_columns = control_tuple
        test_paths, self.AA_columns = test_tuple

        pathlist = control_paths + test_paths

        for RING_path in pathlist:

            data = pd.read_csv(filepath_or_buffer=RING_path, sep="\t", header=0)
            file_name = RING_path.stem
            if file_name not in self.ct_data.columns:
                self.ct_data[file_name]= None #Insert each new file iterated as an empty column in the output dataframe (self.ct_data)
        
            try:
                for _,row in data.iterrows():
                
                    id1 = int(str(row['NodeId1']).split(':')[1])
                    id2 = int(str(row['NodeId2']).split(':')[1])

                    id_set = f"{min(id1, id2)}:{max(id1,id2)}"
                    amino_acid = f"{str(row['NodeId1']).split(":")[3]}:{str(row['NodeId2']).split(":")[3]}" #ILE:SEP
                    missing_bond = pd.isna(row['Interaction']) #Returns (in this case) a Series of all Nan values in the current column of RING data 
                    new_bond = f"{(row['Interaction'])}"

                    if id_set in self.ct_data.index:
                        """
                        Extract any valid bonds that existed previously on that cell, i.e, 
                        multiple chemical bonds established between the amino acids' backbones (HBOND, PIPISTACK)
                        """
                        cell = self.ct_data.loc[id_set, file_name]
                        existing_bond = set(str(cell).split()) if pd.notna(cell) else set() #{HBOND} or {'HBOND', 'VDW'}

                        if (new_bond not in existing_bond) and not missing_bond: 
                            existing_bond.add(new_bond)
                            self.ct_data.loc[id_set, file_name] = " ".join(sorted(existing_bond))

                    #That interaction wasnt scanned before: add to file
                    if id_set not in self.ct_data.index:
                        self.ct_data.loc[id_set, file_name] = None if missing_bond else str(row['Interaction'])
                        self.ct_data.loc[id_set, "ResNum"] = id_set
                        self.ct_data.loc[id_set, "Amino Acid"] = amino_acid

                #self.ct_data = self.ct_data.set_index(["ResNum","Amino Acid"])
                logging.info("PASS: Compare_table datagrame was built successfully")

            except Exception as e:
                logging.error(f"ERROR: Compare_table dataframe wasn't built.")
                #Log failed attempt: any general error in the making of pd.Dataframe. 
                #Stop run cycle if so.
                raise RuntimeError("Critical error from build_table.") from e

        filename = f"compare_table_{now}"
        if interval_check:
            self.select_interval(**kwargs)
            self.file_build(data=self.ct_data, filename=filename)

        elif build_csv:
            self.file_build(data=self.ct_data, filename=filename)

        print("COMPARE (INDEX): ", list(self.ct_data.index.names))
        print("COMPARE (COLUMNS): ", list(self.ct_data.columns)) #if you print with .names, it gives you the COLUMNS ROW index, not the COLUMNS names!!!
