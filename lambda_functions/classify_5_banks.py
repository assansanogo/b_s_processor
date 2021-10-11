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


def download_url(url):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if (".xlsx" in el)][0]
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

    input_file_url = event["url"]
    output_format = event["format"]
    model_path = event["model_path"]
    f_path = download_url(input_file_url)
    model_NLP = import_model(model_path) 

    try:
        # when no error :process and returns json
        dest_file = f_path
        dataframe_file = pd.read_excel(dest_file)
        dataframe_file["Narration_Vectorized"] = dataframe_file["Narration"].apply(lambda x: model_doc2vec.infer_vector(x.split(" "))
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(str(dataframe_file))}

    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}