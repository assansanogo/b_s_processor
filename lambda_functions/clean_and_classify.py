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

def process_descriptions(sentences):
    sentences_from = [re.sub("([\w]+) ([f|F]rom)([\w\W\s]+)", r"\1 from \3", str(el)) for el in sentences]
    sentences_from = [re.sub("([\w]+) ([f|F]rom)([\w\W]+)", r"\1 from \3", str(el)) for el in sentences_from]
    sentences_from = [re.sub("([\w]+) ([v|V]ia)([\w\W\s]+)", r"\1 via \3", str(el)) for el in sentences_from]
    sentences_from = [re.sub("(\s\w{1}\s)","", str(el)) for el in sentences_from]
    sentences_from_no_underscore = [el.replace("_","") for el in sentences_from]
    sentences_from_no_underscore = [(" ").join([et.strip() for et in el.split() if len(et) >1]) for el in sentences_from_no_underscore if not len(el.strip()) <1]
    return sentences_from_no_underscore


def clean_bank_statements(file_name, out_format):
    df = pd.read_csv(file_name)
    df["filtered_description"] = df["filtered_description"].str.upper()
    return df.to_json()
    



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
        processed_dataframe_json = clean_bank_statements(f_name, output_format)
        
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(f_name)}
       
    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
                
    #return process_bank_statements(f_name, output_format)


