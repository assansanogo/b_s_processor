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
    OUTPUT_FILE_NAME = os.environ["output_file_name"]
    OUTPUT_BUCKET_NAME = os.environ["output_bucket_name"]
    
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
        dataframe_file["Narration_Vectorized"] = dataframe_file["Narration"].apply(lambda x: model_Doc2Vec.infer_vector(x.split(" ")))
        dataframe_file["CLASSE"] = dataframe_file["Narration_Vectorized"].apply(lambda x : model_NLP.predict(x.reshape(1, -1)))
        
        s3Client = boto3.client('s3')
        local_filename = '/tmp/classified_file.xlsx'
        dataframe_file.to_excel(local_filename, index=None)
        response = s3_client.upload_file(local_file_name, OUTPUT_BUCKET_NAME, object_name)
        upload_details = s3Client.generate_presigned_url(Bucket=OUTPUT_BUCKET_NAME, Key=OUTPUT_FILE_NAME, ExpiresIn = 100)
        
        
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(str(upload_details))}

    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
