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


# def amazon_recognition (content):
#     client= boto3.client('rekognition', 'eu-west-1')
#     response= client.detect_labels(Image={'Bytes': content}, MaxLabels=10)
#     labels= response['Labels']
#     first_label=labels[0]
#     print("El primer label detectat és {}".format(first_label['Name']))
#     filtered_label = filter_labels(labels)
#     print("El primer label detectat no generic és {}".format(filtered_label['Name']))
#     return first_label, filtered_label #retorna el primer label i el primer label no generenic detectat

# def filter_labels (labels):
#     for label in labels:
#         if label['Name'] not in gen_labels:
#             return label

# def main():
#     file_name = sys.argv[1]
#     with io.open(file_name, 'rb') as image_file:
#         content = image_file.read()
#     first_label, filtered_label = amazon_recognition(content)
#     print("Primer label: {} ({}) \n Primer label no generenic: {} ({})".format(
#         first_label["Name"], 
#         first_label["Confidence"],
#         filtered_label["Name"], 
#         filtered_label["Confidence"]))

# if __name__ == '__main__':
#     main()