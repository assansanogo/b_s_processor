import glob2
import os
import shutil
import tabula
import argparse
from tqdm import tqdm
import pandas as pd



GT_HEADER = ["Trans. Date","Value. Date","Reference","Debits","Credits","Balance","Originating Branch","Remarks"]


def process_bank_statements(b_statement, out_format ='csv'):
    '''
    Method to transform a list of Bank statements paths into a list of .CSV
    '''
    response = {}
    # check the type of b_statements_gt_bank
    if isinstance(b_statement, str):
        b_statement = [b_statement]
    n_statements = len(b_statement)
    assert n_statements !=0
    print(b_statement)
    #loop over the list of bank statements 
    for idx, bk_st in tqdm(enumerate(b_statement)):
        #input filename
        inp = bk_st
        local_inp = inp.split("/")[-1]
        shutil.copy(inp, local_inp )
        
        #output filename
        out = bk_st.replace(".pdf","_output.csv")
        
        # convert to csv by default
        df = tabula.read_pdf(bk_st, multiple_tables=True, lattice= True, pages='all')
        header_shape = df[1].shape[1]
        df_list = [dataframes for dataframes in df if dataframes.shape[1] !=2]
        for i,d in enumerate(df_list):
            try:
                d.columns = GT_HEADER
                d.to_csv(out.replace(".csv",f"{str(i)}.csv"), sep=';')
            except Exception as e:
                print(i)
                df_list.remove(d)
        response[str(idx)] = {"name":bk_st, "body":[d.reset_index(drop=True).to_json() for d in df_list]}
        return response
        
        
if __name__ =='__main__':
    
    liberta_leasing_parser = argparse.ArgumentParser()
    liberta_leasing_parser.add_argument('--input_file', action='store', type=str, required=True)
    liberta_leasing_parser.add_argument('--output_format', action='store', type=str, required=True, default='csv')
    
    args = liberta_leasing_parser.parse_args()
    f_name = args.input_file
    output_format = args.output_format
    process_bank_statements(f_name, output_format)
