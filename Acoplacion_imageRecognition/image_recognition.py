import io
import os
import boto3


def amazon_recognition ():
	file_name = os.path.join(os.path.dirname(__file__), 'ingredient.jpg')

	client= boto3.client('rekognition', 'eu-west-1')
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()
	response= client.detect_labels(Image={'Bytes': content}, MaxLabels=10)
	labels= response['Labels']
	label=labels[0]
	print 'Estic dins amazon_recognition'
	print("El primer label detectat es {}".format(label['Name']))
	return label['Name'] #retorna el primer label detectat