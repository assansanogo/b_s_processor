import os
import json
import shutil

import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import glob2
import requests
import base64
from zipfile import ZipFile
from tqdm import tqdm
import gensim
import joblib
import pandas as pd


def download_url(url, ext):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if (f".{ext}" in el)][0]
    os.makedirs('/tmp', exist_ok=True)
    
    # open a file to dump the stream in
    print(r)
    print(file_name)
    
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(os.stat(f'/tmp/{file_name}').st_size)

    return f'/tmp/{file_name}'
  

def import_model(model_path):
    model_Doc2vec = gensim.models.Doc2Vec.load(model_path)
    return model_Doc2vec


  # problem with pngs
  
def classify_liberta_leasing_convert_handler(event, context):
    '''
    function whose responsibility is to classify
    '''

    if 'body' in list(event.keys()):
        event = json.loads(event['body'])
    
    OUTPUT_FILE_NAME = event["output_file_name"]
    OUTPUT_BUCKET_NAME = event["output_bucket_name"]
    input_file_url = event["url"]
    output_format = event["format"]
    model_Doc2Vec_path = event["model_Doc2Vec_path"]
    model_NLP_path = event["model_NLP_path"]
    
    local_model_Doc2Vec_path = download_url(model_Doc2Vec_path, "model")
    model_Doc2Vec = import_model(local_model_Doc2Vec_path) 
    
    local_model_NLP_path = download_url(model_NLP_path,"pkl")
    model_NLP = joblib.load(local_model_NLP_path)
    
    f_path = download_url(input_file_url, "xlsx")
    

    try:
        # when no error :process and returns json
        dest_file = f_path
        dataframe_file = pd.read_excel(dest_file)
        # the narration columns varies from 1 bank to another
        bank_columns = { "WEMA_BANK": "Narration",
                         "UBA_BANK":"Narration",
                         "STANDARD_CHARTERED_BANK": "Transaction",
                         "POLARIS_BANK":"Details",
                         "ACCESS_BANK":"Description"}
        
        column_name = bank_columns[output_format]        
            
        dataframe_file["Narration_Vectorized"] = dataframe_file[column_name].apply(lambda x: model_Doc2Vec.infer_vector(x.split(" ")))
        dataframe_file["CLASSE"] = dataframe_file["Narration_Vectorized"].apply(lambda x : model_NLP.predict(x.reshape(1, -1))[0])
        dataframe_file["BANK_ID"] = output_format
        
        s3_client = boto3.client('s3')
        local_file_name = '/tmp/classified_file.xlsx'
        dataframe_file.to_excel(local_file_name, index=None)
        
        response = s3_client.upload_file(local_file_name, OUTPUT_BUCKET_NAME, OUTPUT_FILE_NAME)
        upload_details = s3_client.generate_presigned_url('get_object', Params={"Bucket":OUTPUT_BUCKET_NAME, "Key":OUTPUT_FILE_NAME}, ExpiresIn = 100)
        
        
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(str(upload_details))}

    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
