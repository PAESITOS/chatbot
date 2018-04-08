# Image Recognition
## How-To Amazon Rekognition python code
client=boto3.client('rekognition','eu-west-1')

with open(imageFile, 'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()})

first_label = response['Labels'][0]
first_label_name = first_label["Name"]
first_label_confidence = first_label["Confidence"]