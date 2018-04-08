import sys

from mfamazon import most_frequent_amazon as gen_labels

import boto3




if __name__ == "__main__":

    imageFile = sys.argv[1]

    client=boto3.client('rekognition','eu-west-1')

    with open(imageFile, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
        
    print('Detected labels in ' + imageFile)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))

    print('"Filtered" label in ' + imageFile)    
    for label in response['Labels']:
        if label['Name'] not in gen_labels:
            print (label['Name'] + ' : ' + str(label['Confidence']))
            break

    print('Done...')