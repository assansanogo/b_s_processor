#!/usr/bin/env python


import os
import shutil
import sklearn
from tqdm import tqdm
import pandas as pd
import numpy as np
import requests
import json
import base64

__author__ = "Assan Sanogo"
__copyright__ = "Copyright 2007, Liberta Leasing"
__credits__ = ["Liberta Leasing", "Assan Sanogo"]
__license__ = "private"
__version__ = "0.1"
__maintainer__ = "Assan Sanogo"
__email__ = "predicteev@gmail.com"
__status__ = "Production"

def download_url(url, extension="csv"):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if f".{extension}" in el][0]
    # open a file to dump the stream in
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    return f'/tmp/{file_name}'

def liberta_leasing_classify_handler(event, context):
    '''
    formatting of the lambda handler to be compatible with by AWS
    '''
    # information extracted from the event payload
    input_file_url = event["url"]
    output_format = event["format"]
    
    # download file locally and keep the filename
    f_name = download_url(input_file_url)
    
    try:
        # when no error :process and returns json
        processed_dataframe = process_bank_statements(f_name, output_format)
        
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(f_name)}
       
    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
                
    #return process_bank_statements(f_name, output_format)


