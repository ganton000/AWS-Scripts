from chalice import Chalice
from chalicelib import storage_service
from chalicelib import recognition_service
import sys
import random

app = Chalice(app_name='Capabilities')
app.debug = True

storage_location = "contents.anton.ai"
storage_service = storage_service.StorageService(storage_location)
recognition_service = recognition_service.RecognitionService(storage_service)

@app.route('/demo-object-detection', cors=True)
def demo_object_detection() -> dict:
    '''
    Randomly selects an image for object detection
    '''
    files = storage_service.list_files()
    images = [ file for file in files if file['file_name'].endswith(".jpg") ]
    image = random.choice(images)

    print('filename:', image['file_name'])
    objects = recognition_service.detect_objects(image['file_name'])

    return {
        "imageName" : image['file_name'],
        "imageUrl" : image['url'],
        "objects" : objects
    }