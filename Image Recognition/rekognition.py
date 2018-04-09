
## --- ACCURACY TEST --- ##
""" 
This script moves through the dataset of ingredients 
and uses the google vision and amazon rekognition service to obtain the labels.
Compare the two services and gives a file with all the data recolected.
"""

# -- IMPORTED LIBRARIES -- # 
import io
import os
import boto3
import pickle
import random

from pathlib import Path
from google.cloud import vision
from google.cloud.vision import types

# -- DEFINING THE RESULTS DICTIONARY -- #
results = {'punt_google':0,
        'punt_amazon':0,
        'file_name':[],
        'pos_google':[],
        'pos_amazon':[],
        'score_google':[],
        'score_amazon':[]
        }
google_words = {}
amazon_words = {}

# -- FUNCTION DEFINITIONS -- #

def amazon_accuracy(rekognition_client,content,real_label):
    """ 
    This function calculates the accuracy given by the amazon rekognition service
        by one image. We valorate relevant information. 
    """
    keys = amazon_words.keys()
    response = rekognition_client.detect_labels(Image={'Bytes': content},MaxLabels=10)
    labels = response['Labels']
    counter = 0
    pos=11
    score=0.0
    for label in labels:
        counter += 1
        if real_label == label['Name'].lower():
            pos = counter
            score=(11-counter)/10
        else:
            if label['Name'] in keys:
                amazon_words[label['Name']] += 1
            else:
                amazon_words[label['Name']] = 1
    return score, pos

def obtaining_results(data_directory,vision_client,rekognition_client):
    """ 
    This function moves through directories in the DataSet and gets the position
        and score of both (google & amazon) services from the images of the DataSet. 
    """
    for path in data_directory.iterdir():
        if path.is_dir():
            for ingredient in path.glob('*.jpg'):
                file_name = str(path.joinpath(ingredient.name))
                real_label = ingredient.name[:-7]       
                with io.open(file_name,'rb') as image_file:
                    content = image_file.read()
                    image = types.Image(content=content)
                # -- CALLING GOOGLE & AMAZON SERVICES -- #
                s_amazon,p_amazon = amazon_accuracy(rekognition_client,content,real_label)
                print(file_name)
                # -- OBTAINING RESULTS FOR ONE IMAGE -- #
                results['file_name'].append(ingredient.name[:-4])
                results['pos_amazon'].append(p_amazon)
                results['score_amazon'].append(s_amazon)
                
def main():
    """ 
    The main program gets the images from the dataset
        and evaluates how the google vision services operates. 
    """
    # -- SETTING THE DIRECTORIES -- #
    data_directory = Path.cwd() / 'DataSet'

    # -- SERVICES CLIENTS -- #
    rekognition_client = boto3.client('rekognition','eu-west-1')

    # -- ACCESING TO THE DATASET IMAGES -- #
    obtaining_results(data_directory,vision_client,rekognition_client)

    # -- SAVING VARIABLE RESULTS IN A PICKLE -- #
    with open('results.pkl','wb') as file:
        pickle.dump(results,file)
    file.close()
    with open('google_words.pkl','wb') as file:
        pickle.dump(google_words,file)
    file.close()
    with open('amazon_words.pkl','wb') as file:
        pickle.dump(amazon_words,file)
    file.close()
    
if __name__ == '__main__':
    main()