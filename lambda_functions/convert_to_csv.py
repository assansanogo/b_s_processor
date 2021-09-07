def process_bank_statements(b_statements_gt_bank, out_format ='csv'):
    '''
    Method to transform a list of Bank statements paths into a list of .CSV
    '''
    # check the type of b_statements_gt_bank
    if type(b_statements_gt_bank) =='str':
      b_statements_gt_bank = list(b_statements_gt_bank)
    n_statements = len(b_statements_gt_bank)
    assert len(n_statements) !=0
    
    #loop over the list of bank statements 
    for bk_st in tqdm(b_statements_gt_bank):
        #input filename
        inp = bk_st
        #output filename
        out = bk_st.replace(".pdf","_output.csv")
        # convert to csv by default
        tabula.convert_into(inp, out, output_format=out_format)
  
