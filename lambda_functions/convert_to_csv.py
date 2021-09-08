import glob2
import os
import shutil
import tabula
import argparse
from tqdm import tqdm
import pandas as pd



GT_HEADER = ["Trans. Date","Value. Date","Reference","Debits","Credits","Balance","Originating Branch","Remarks"]


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
    transactions_df = m_df[~m_df["Trans. Date"].isna().copy()
    transactions_idx = list(transactions_df.index())
    max_transactions_idx = max(transactions_idx)
    transactions_df.loc[max_idx + 1,'Trans. Date'] = '99-Apr-9999'
    return  transactions_df,transactions_idx,max_transactions_idx
                           
                           
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
        df_list = [datafram for datafram in df_list if (datafram.shape[1] !=2 and datafram.shape[0]!=0) ]
        for i,d in enumerate(df_list):
            try:
                # set the header to each sub dataframe
                d.columns = GT_HEADER
                # save locally for debug purposes
                d.to_csv(out.replace(".csv",f"{str(i)}.csv"), sep=';')
            except Exception as e:
                # if the dataframe is malformed remove it from the list of processable dataframes
                print(i)
                df_list.remove(d)
        
        # concat each dataframe
        master_df = pd.concat(df_list)
                           
        # clean non informative cells
        master_df = simple_df_clean(master_df)
        
        # store informations about the transactions
        tr_df, tr_idx, max_tr_idx = transactions(master_df)
        
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
