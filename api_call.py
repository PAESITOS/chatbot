import json
import requests
import urllib

def spoonacular_api_call( method, url, token, parameters):
    #Param payload es para los 'POST'
    """
    :param instruction:
    :param method:
    :param url:
    :param token: <str>
    :param payload:  
    :param parameters:
    :return:
    """
    headers = {"X-Mashape-Key": token,
               'Accept': 'application/json',
                }
    
    encoded_parameters = urllib.urlencode(parameters)
    url = url + encoded_parameters
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers)

    # else: #method.upper() == 'POST':
    #     response = requests.post(url, headers=headers, data=json.dumps(payload), params=parameters)
    return response