from mfamazon import most_frequent_amazon as gen_labels
import io, os, sys
import boto3

def amazon_recognition (photo):
    client = boto3.client('rekognition', 'eu-west-1')
    response = client.detect_labels(Image={'Bytes': photo}, MaxLabels=10, MinConfidence=0)
    labels = response['Labels']
    first_label = labels[0]
    print("El primer label detectat es {}".format(first_label['Name']))
    filtered_label = filter_labels(labels)
    if filtered_label is None:
        return None
    else:
        return filtered_label #retorna el primer label i el primer label no generenic detectat

def filter_labels (labels):
    for label in labels:
        if label['Name'] not in gen_labels:
            return label
    return None
