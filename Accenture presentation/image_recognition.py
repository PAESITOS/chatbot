from mfamazon import most_frequent_amazon as gen_labels
import io, os, sys
import boto3

def amazon_recognition ():
    client= boto3.client('rekognition', 'eu-west-1')
    with io.open('ingredient.jpg', 'rb') as image_file:
        content = image_file.read()
    response= client.detect_labels(Image={'Bytes': content}, MaxLabels=10, MinConfidence=0)
    labels= response['Labels']
    first_label=labels[0]
    print("El primer label detectat es {}".format(first_label['Name']))
    filtered_label = filter_labels(labels)
    if filtered_label is None:
        print("Malas labels")
    else:
        print("El primer label detectat no generic es {}".format(filtered_label['Name']))
        return filtered_label['Name'] #retorna el primer label i el primer label no generenic detectat

def filter_labels (labels):
    for label in labels:
        print(type(label['Name']))
        if label['Name'] not in gen_labels:
            print(label['Name'])
            return label
    return None
