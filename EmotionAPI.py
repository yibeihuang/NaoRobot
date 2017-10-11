import time 
import requests
import cv2
import operator
import numpy as np
import json

# Variables

with open('config.json') as f:
        data = json.load(f)
_url = data.get("_url").encode("utf-8")
_key = data.get("_key").encode("utf-8")
_maxNumRetries = 10

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result

def get_emotion(pathToFileInDisk):
    # Load raw image file into memory
    # pathToFileInDisk = r'/Users/yibeihuang/Pictures/yibei_pp.jpg'
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None
    params = None

    result = processRequest( json, data, headers, params )
    print result
    if result != []:
        emotions = result[0].get('scores')
        minval = -1
        for key,val in emotions.iteritems():
            if val>minval: emotion, minval = key, val
        print emotion
        return emotion
    else: return None
    
if __name__ == '__main__':
    get_emotion(pathToFileInDisk)

