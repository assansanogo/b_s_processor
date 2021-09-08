import glob2
import os
import shutil
import tabula
import argparse
from tqdm import tqdm
import pandas as pd
import numpy as np



GT_HEADER = ["Trans. Date","Value. Date","Reference","Debits","Credits","Balance","Originating Branch","Remarks"]

def extract_list_dataframes(dataframes_list, out_path):
    
    for i,d in enumerate(dataframes_list):
        try:
            # set the header to each sub dataframe
            d.columns = GT_HEADER
            # save locally for debug purposes (each extracted dataframe has a positional suffix (=index))
            d.to_csv(out_path.replace(".csv",f"{str(i)}.csv"), sep=';')
        except Exception as e:
            # if the dataframe is malformed remove it from the list of processable dataframes
            print(i)
            dataframes_list.remove(d)
    return dataframes_list

def simple_df_clean(m_df):
    '''
    function which cleans non informative data ("Remarks and Trans.date")
    ocurring while tabula extraction
    '''
    m_df = m_df[m_df['Remarks']!= 'Remarks']
    m_df = m_df[m_df['Remarks']!= 'Balance as at Last Transaction.']
    m_df = m_df[m_df["Trans. Date"] != 'Trans. Date']
    return m_df

def transactions(m_df):
    '''
    function which keeps transactions index, the last transaction idx and adds an artificial last transaction
    '''
    transactions_df = m_df[~m_df["Trans. Date"].isna()].copy()
    transactions_idx = list(transactions_df.index())
    max_transactions_idx = max(transactions_idx)
    transactions_df.loc[max_transactions_idx + 1,'Trans. Date'] = '99-Apr-9999'
    return  transactions_df,transactions_idx,max_transactions_idx
                           
                           
def postprocess(m_df, transaction_not_null):
    '''
    reconstruct the financial operations which overflow to the next line in 1 single text
    '''

    # all the indexes of the transaction with dates
    index_with_dates = transaction_not_null.index

    operation_descr = {}
    for step_date in index_with_dates:
        operation_descr[str(step_date)] = []
    
    # safety check : index is not nan                       
    if not np.isnan(index_with_dates.values[0]):

        for idx, step in enumerate(index_with_dates):
            # iteration until we reach the last recorded transaction (excluded)
            if idx < len(index_with_dates)-1:
                for ind in range(index_with_dates[idx], index_with_dates[idx+1], 1):
                    if str(m_df.loc[ind, 'Remarks']) != 'nan':
                        operation_descr[str(step)] += [str(m_df.loc[ind, 'Remarks'])]
                           
            # last iteration: after reaching the last recorded transaction until the artificial last operation
            else:
                for ind in range(index_with_dates[idx], m_df.shape[0], 1):
                    if str(m_df.loc[ind, 'Remarks']) != 'nan':
                        operation_descr[str(step)] += [str(m_df.loc[ind, 'Remarks'])]
        # final cleanup (remove carriage to prevent csv malformation)
        for key in operation_descr.keys():
            operation_descr[key] = (''.join(operation_descr[key])).replace('\r',' ')

    return operation_descr                       
                           
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
                           
    #loop over the list of bank statements 
    for idx, bk_st in tqdm(enumerate(b_statement)):
        #input filename
        inp = bk_st
        local_inp = inp.split("/")[-1]
        shutil.copy(inp, local_inp )
        
        #output filename
        out = bk_st.replace(".pdf","_output.csv")
        
        # convert to csv by default
        df_list = tabula.read_pdf(bk_st, multiple_tables=True, lattice= True, pages='all')
        header_shape = df_list[1].shape[1]
        df_list = [datafram for datafram in df_list if (header_shape !=2 and datafram.shape[0]!=0) ]
                           
        # extract dataframes & save to disk for debug                 
        df_list = extract_list_dataframes(df_list, out)
        
        # concat each dataframe
        master_df = pd.concat(df_list)
                           
        # clean non informative cells
        master_df = simple_df_clean(master_df)
        
        # store informations about the transactions
        tr_df, tr_idx, max_tr_idx = transactions(master_df)
                     
        # postprocessing of transactions 
        postprocess(master_df, tr_df)
        
        # json response
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
