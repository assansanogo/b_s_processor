import pandas as pd
from pathlib import Path
import shutil
import glob2
import random
import time
import cv2
import numpy as np
import requests
import json
import base64
from zipfile import ZipFile
import os


def download_url(url):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if (".zip" in el)][0]
    os.makedirs('/tmp', exist_ok=True)
    # open a file to dump the stream in
    print(r)
    print(file_name)
    
    with open(f'/tmp/{file_name}', 'wb') as fd:
        
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(os.stat(f'/tmp/{file_name}').st_size)
    
    with ZipFile(f'/tmp/{file_name}', 'r') as zip:
        # extracting all the files
        print(zip.namelist())
        os.makedirs(f'/tmp/all_csv/{file_name}', exist_ok=True)
        os.chdir('/tmp/all_csv')
        
        for file_zip in zip.namelist():
            zip.extract(file_zip,f'/tmp/all_csv')
        print('Extracting all the files now...')
        
        
        
        
    print(os.getcwd())
    print(glob2.glob(os.getcwd()+'/*'))
    print(glob2.glob('/tmp/all_csv/*'))
    file_path = file_name.replace(".zip","")
    print(glob2.glob(f'/tmp/all_csv/{file_path}/*'))
        
    return f'/tmp/all_csv/{file_path}'


def guess_header(all_csv):
    
    
    header_types = get_info() 
    filtered_csv = []
    for el in all_csv:
        try:
            cols = list(pd.read_csv(el, error_bad_lines=False).columns)
            cols = [col.strip() for col in cols if "Unnamed" not in col]
            filtered_csv.append(cols)
        except:
            pass

    mitsuketa = False

    for el in filtered_csv[:100]:
        if mitsuketa:
            break
        else:
            for header in header_types:
                if el == header:
                    dataframe_header = header
                    mitsuketa = True
                    break
                else:
                    #print(el)
                    dataframe_header = None

    return(dataframe_header)



def get_info() :
    header_type_1 = ["TXN DATE" ,"VAL DATE" ,"REMARKS" ,"DEBIT" ,"CREDIT" ,"BALANCE"]
    header_type_2 = ["POSTING DATE" ,"VALUE DATE" ,"DESCRIPTION" ,"OUTFLOW" ,"INFLOW" ,"BALANCE"]
    header_type_3 = ["Date" ,"Transaction" ,"Deposit" ,"Withdrawal" ,"Closing Balance"]
    header_type_4 = ["TRANS DATE" ,"VALUE DATE" ,"NARRATION" ,"CHQ. NO" ,"DEBIT" ,"CREDIT" ,"BALANCE"]
    header_type_5 =['Posted Date', 'Value Date', 'Description', 'Debit', 'Credit', 'Balance']
    header_type_6 = ["Posted Date" ,"Description" ,"Value Date" ,"Withdrawal" ,"Deposit","Balance"]
    header_type_7 = ["Tran date" ,"Transaction ID" ,"Narration" ,"Withdrawal","Deposit","Running Balance"]
    header_type_8 = ["DATE POSTED" ,"VALUE DATE" ,"DESCRIPTION" ,"DEBIT" ,"CREDIT" ,"BALANCE"]
    header_type_9 = ["Transaction Date" ,"Value Date" ,"Cheque Number" ,"Transaction Remarks" ,"Amount Type" ,"Withdrawal" ,"Deposits" ,"Account Balance"]
    header_type_10 = ["Ref #" ,"P/Date" ,"V/Date" ,"Narration Chq/Instr. #" ,"Debit" ,"Credit" ,"Balance"]
    header_type_11 = ["Trans Date" ,"Refe." ,"Value Date" ,"Debit" ,"Credit" ,"Balance" ,"Remarks"]
    header_type_12 = ["Trans. Date" ,"Value. Date" ,"Reference" ,"Debits" ,"Credits" ,"Balance" ,"Originating Branch" ,"Remarks"]
    header_type_13 = ["Date" ,"V. Date" ,"Narration" ,"Ref" ,"Debit" ,"Credit" ,"Balance" ]
    header_type_14 =["EntryDate" ,"Details" ,"ValueDate" ,"Debit" ,"Credit" ,"Balance"]
    header_type_15 = ["DATE" ,"NARRATIVE" ,"REFERENCE" ,"VALUE DATE" ,"WITHDRAWLS" ,"LODGEMENTS" ,"BALANCE"]
    header_type_16 = ['Trans Date', 'Ref. Number', 'Transaction Details', 'Value Date', 'Withdrawal(DR)', 'Deposit(CR)', 'Balance']

    header_types =[header_type_1,
                  header_type_2,
                  header_type_3,
                  header_type_4,
                  header_type_5,
                  header_type_6,
                  header_type_7,
                  header_type_8,
                  header_type_9,
                  header_type_10,
                  header_type_11,
                  header_type_12,
                  header_type_13,
                  header_type_14,
                  header_type_15,
                  header_type_16,
                  ]

    column_mapper ={
        "TRANSACTION_DATE":["DATE", "POSTING DATE","P/Date", "TRANS DATE", "Posted Date", "Tran date",
                            "Trans Date","Trans. Date" "DATE POSTED", "Transaction Date","EntryDate",
                            "TXN DATE"],
        "VALUE_DATE":["VALUE_DATE","Value Date","Value. Date","V/Date","V. Date","ValueDate"],
        "REFERENCE": ["REFERENCE","Ref #","Refe.","Reference","Ref", "Transaction ID",
                     'Ref. Number'],
        "DEBIT":["DEBIT","OUTFLOW","Debit", "Debits"],
        "CREDIT":["CREDIT","INFLOW","Credit", "Credits"],
        "DEPOSIT": ["DEPOSIT","Deposits","Deposit", 'Deposit(CR)'],
        "WITHDRAWAL":["WITHDRAWLS","WITHDRAWLS",'Withdrawal(DR)'],
        "BALANCE":["BALANCE","Closing Balance","Running Balance","Balance", "Account Balance"],
        "CHEQUE": ["CHEQUE","CHQ. NO","Cheque Number"],
        "DESCRIPTION":["DESCRIPTION","Narration Chq/Instr. #","Narration",
                       "NARRATION", "Transaction Remarks", "REMARKS", "Remarks",
                      "DETAILS", "Details",'Transaction Details']  
    }
    return header_types




global_dump = []
def check_out_path(target_path, my_dir='', selected_ext ='png'):
    global global_dump
    """"
    This function recursively lists all contents of a pathlib.Path object
    """
    def give_full_path(my_file, my_dir, ext=None):
        if (ext != None and my_file.name.endswith(ext)):
            global_dump.append(my_file.resolve())

    #give_full_path(target_path.name, my_dir)
    
    for file in target_path.iterdir():
        if file.is_dir():
            check_out_path(file, my_dir)
        else:
            
            give_full_path(file, my_dir, selected_ext)





def process_csv(input_folder, bank_name=None):
    files_csv = f'{input_folder}/*.csv'
    
    file_dest = f'{input_folder}/final_parsed.xlsx'
    l_csv = glob2.glob(files_csv)
    l_csv = sorted(l_csv)
    data_csv = []
    len_csv = []

    for i in range(len(l_csv)):
        with open(l_csv[i]) as f:
            datum = (f.readlines()) 
            print(datum)
            if bank_name in ["UBA_BANK","STANDARD_CHARTERED_BANK", "WEMA_BANK"]:
                datum = [el.replace(",,"," , , ") for el in datum]
            datum_values = [el.split(" ,") for el in datum if (not "Balance B/F." in el and not "Opening Balance" in el and not 'Closing Balance' in el and not "Total" in el)]


            datum_values = [[sub_el for sub_el in el if sub_el != '\n'] for el in datum_values]
            
            print("#csv contents")
            print(datum_values)
            
            
            for idx, el in enumerate(datum_values):
                if idx >0:
                    try:
                        val = datum_values[idx][1].split(",")
                        if len(val)==1:
                            val = val[0]
                        datum_values[idx][1] = val
                    except IndexError:
                        pass

            datum_values = pd.DataFrame(datum_values)
        data_csv.append(datum_values)

    len_csv.append([len(el) for el in data_csv])
    concatenated = pd.concat(data_csv)
    
    concatenated.columns = concatenated.iloc[0]
    data_columns = [col for col in concatenated.columns if col != '\n']
    
    if bank_name == "POLARIS":
        concatenated = concatenated[data_columns]
        concatenated = concatenated.drop(concatenated.index[0]).reset_index(drop=True)
        concatenated.columns = guess_header(l_csv )
        
    if bank_name == "ACCESS_BANK":
        concatenated = concatenated[data_columns]
        concatenated = concatenated.drop(concatenated.index[0]).reset_index(drop=True)
        concatenated.columns = guess_header(l_csv )
        concatenated.to_excel(file_dest)
    if bank_name == "UBA_BANK":
        concatenated = concatenated[data_columns]
        concatenated = concatenated.drop(concatenated.index[0]).reset_index(drop=True)
        concatenated.columns = guess_header(l_csv )
        concatenated.to_excel(file_dest)
    if bank_name == "STANDARD_CHARTERED_BANK":
        concatenated = concatenated[data_columns]
        concatenated = concatenated.drop(concatenated.index[0]).reset_index(drop=True)
        concatenated.columns = guess_header(l_csv )
        concatenated.to_excel(file_dest)
    
    if bank_name == "WEMA_BANK":
        concatenated = concatenated[data_columns]
        concatenated = concatenated.drop(concatenated.index[0]).reset_index(drop=True)
        n_cols = guess_header(l_csv) 
        concatenated = concatenated.iloc[:, :len(n_cols)]
        concatenated.columns = guess_header(l_csv )
        concatenated.to_excel(file_dest)
    
    return concatenated

def liberta_leasing_convert_handler(event, context):
    '''
    formatting of the lambda handler to be compatible with by AWS
    '''
    # information extracted from the event payload
    
    if "body" in event.keys():
        event = json.loads(event["body"])
                           
    zip_url = event["url"]
    bank_format = event["format"]
    
    
    # download file locally and extract a zip
    f_path = download_url(zip_url)

     
    try:
        # when no error :process and returns json
        #processed_dataframe = process_bank_statements(f_name, bank_format)
        output_file = process_csv(f_path, bank_format)
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(output_file.to_string())}
       
    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
                
