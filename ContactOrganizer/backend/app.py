from chalice import Chalice
from chalicelib import storage_service
from chalicelib import recognition_service
from chalicelib import extraction_service
from chalicelib import contact_store

import base64
import json

app = Chalice(app_name='Capabilities')
app.debug = True

#services initialization
storage_location = 'contents.anton.ai'
storage_service = storage_service.StorageService(storage_location)
recognition_service = recognition_service.RecognitionService(storage_location)
extraction_service = extraction_service.ExtractionService()
store_location = 'Contacts'
contact_store = contact_store.ContactStore(store_location)

#RESTful endpoints
@app.route('/images/{image_id}/extract-info', methods=['POST'], cors=True)
def extract_image_info(image_id):
    '''
    Detects text in the specified image
    Then extracts contact information from the text
    '''
    MIN_CONFIDENCE = 70.0

    text_lines = recognition_service.detect_text(image_id)

    contact_lines = []
    for line in text_lines:
        #check confidence
        if float(line['confidence']) >= MIN_CONFIDENCE:
            contact_lines.append(line['text'])

        contact_string = '  '.join(contact_lines)
        contact_info = extraction_service.extract_contact_info(contact_string)

    return contact_info

@app.route('/contacts', methods = ['POST'], cors = True)
def save_contact():
    """saves contact information to the contact store service"""
    request_data = json.loads(app.current_request.raw_body)

    contact = contact_store.save_contact(request_data)

    return contact


@app.route('/contacts', methods = ['GET'], cors = True)
def get_all_contacts():
    """gets all saved contacts in the contact store service"""
    contacts = contact_store.get_all_contacts()

    return contacts

@app.route('/images', methods = ['POST'], cors = True)
def upload_image():
    """processes file upload and saves file to storage service"""
    request_data = json.loads(app.current_request.raw_body)
    file_name = request_data['filename']
    file_bytes = base64.b64decode(request_data['filebytes'])

    image_info = storage_service.upload_file(file_bytes, file_name)

    return image_info
