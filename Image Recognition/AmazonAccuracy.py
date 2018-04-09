# ACCURACY TEST

""" This script moves through the dataset of ingredients 
and uses the google vision service to obtain the labels.
We will have to determine which is the results
"""

# -- IMPORTING LIBRARIES -- # 
import io
import os

import boto3
from pathlib import Path


# -- FUNCTION DEFINITIONS -- #       
def amazon_accuracy(content,real_label,client):
    response = client.detect_labels(Image={'Bytes': content})
    labels = response['Labels']
    for label in labels:
        if real_label == label['Name'].lower():
            return label['Confidence']
    return 0.0

def main():
    main_directory = Path.cwd()
    # -- AMAZON APPLICATION CREDENTIALS -- #
    client = boto3.client('rekognition','eu-west-1')
    data_directory = main_directory / 'DataSet'

    score_avg_amazon = 0
    i = 0
    cont_fallo = 0

    for path in data_directory.iterdir():
        if path.is_dir():
            real_label = path.name.lower()
            for ingredient in path.glob('*.jpg'):
                file_name = str(path.joinpath(ingredient.name))
                print(file_name)
                with io.open(file_name,'rb') as image_file:
                    content = image_file.read()
                score = amazon_accuracy(content,real_label,client)
                print(str(score))
                if score==0.0:
                    cont_fallo += 1
                else:
                    score_avg_amazon += score
                i += 1
    print('Score medio: ' + str(score_avg_amazon/i) + '\nFallos:' + str(cont_fallo))
    
if __name__ == '__main__':
    main()
