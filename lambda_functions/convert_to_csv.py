import glob2
import shutil
import tabula
import argparse
from tqdm import tqdm

def process_bank_statements(b_statements_gt_bank, out_format ='csv'):
    '''
    Method to transform a list of Bank statements paths into a list of .CSV
    '''
    # check the type of b_statements_gt_bank
    if type(b_statements_gt_bank) =='str':
      b_statements_gt_bank = list(b_statements_gt_bank)
    n_statements = len(b_statements_gt_bank)
    assert n_statements !=0
    
    #loop over the list of bank statements 
    for bk_st in tqdm(b_statements_gt_bank):
        #input filename
        inp = bk_st
        local_inp = inp.split("/")[-1]
        shutil.copy2(local_inp, os.getcwd())

        #output filename
        out = bk_st.replace(".pdf","_output.csv")
        # convert to csv by default
        tabula.convert_into(inp, out, out_format)
        
        
        
if __name__ =='__main__':
    
    liberta_leasing_parser = argparse.ArgumentParser()
    liberta_leasing_parser.add_argument('--input_file', action='store', type=str, required=True)
    liberta_leasing_parser.add_argument('--output_format', action='store', type=str, required=True, default='csv')
    
    args = liberta_leasing_parser.parse_args()
    f_name = args.input_file
    output_format = args.output_format
    process_bank_statements(f_name, output_format)
  
