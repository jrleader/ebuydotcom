# handlers/file.py

from ast import Try
from concurrent.futures import ThreadPoolExecutor
from importlib.util import resolve_name
from os import path
from turtle import down
from urllib import response

from flask import Blueprint, request, current_app
from werkzeug.wsgi import wrap_file
from werkzeug.exceptions import NotFound
from gridfs import GridFS
from gridfs.errors import NoFile
from flask_pymongo import BSONObjectIdConverter
from bson import objectid

from tblib.mongo import mongo
from tblib.handler import json_response, ResponseCode

from ..models import FileSchema

from os import path, unlink
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO, BufferedReader

from PIL import Image

file = Blueprint('file', __name__, url_prefix='')

def make_thumbnails(id):
    # file = None
    try:
        file = GridFS(mongo.db).get(objectid.ObjectId(id))
        print('file: {}, id: {}'.format(file, id))
    except NoFile as gridfs_error:
        print(gridfs_error)
        raise NotFound()
    
    print('Making thumbnails...')
    print(file)
    if file:
        img = Image.open(file)
        print(img)
        thumbnails = {}
        for size in (1024,512,200):
            print(size)
            t = img.copy()
            try:
                t.thumbnail((size,size)) # Make thumbnail with PIL
                filename = '{}_{}.jpg'.format(id, size)
                filepath = './{}'.format(filename) 
                t.save(filepath, 'JPEG')
                print('thumbnail with size {} size saved'.format(size))
                with open(filepath, 'rb') as f:
                    thumbnails['{}'.format(size)] = mongo.save_file(filename, f)
                unlink(filepath)
            except Exception as e:
                print(e)
        print(thumbnails)
        mongo.db.fs.files.update({'_id': id}, {'$set' : {
            'thumbnails': thumbnails
        }
        })
        print('Thumbnail of img {} has been created!'.format(id))
    else: raise NotFound()
    # print('Thumbnail of img {} has been created!'.format(id))


@file.route('/files', methods=['POST'])
def create_file():
    '''
    Upload file to GridFS upon form submission
    '''
    global executor
    executor = ThreadPoolExecutor(max_workers=2) # Making a separate thread for thumbnail generaation
    # Do not save the file if the file to be uploaded is empty
    if 'file' not in request.files or request.files['file'].filename == '':
        raise NotFound()

    # Upload the file
    id = mongo.save_file(request.files['file'].filename, request.files['file'])

    # with ThreadPoolExecutor(max_workers=2) as executor:
    # Generate thumbnails in a separate thread
    # executor.submit(lambda: make_thumbnails(id))
    executor.submit(make_thumbnails,id)

    # Get file extension
    _, ext = path.splitext(request.files['file'].filename)

    # Generate json response
    return json_response(id='{}{}'.format(id, ext))


@file.route('/files/<id>', methods=['GET'])
def file_info(id):
    '''
    Get file info
    '''

    id, _ = path.splitext(id) # Get the file id

    id = BSONObjectIdConverter({}).to_python(id) # Convert id string to id object

    try: # Get the file info from GridFS
        file = GridFS(mongo.db).get(id)
    except NoFile:
        raise NotFound()
    
    file = FileSchema().dump(file) # Convert file obj to dict
    return json_response(file=file)

def file_response(id, download=False):
    '''
    *****
    IMPORTANT !!!
    *****
    Configure the response containing the file itself
    '''
    try:
        file = GridFS(mongo.db).get(id)
    except NoFile:
        raise NotFound()

    # global BUFFER_SIZE 
    BUFFER_SIZE = 1024 * 255
    CACHE_KEEP_ALIVE_TIME = 365*24*3600 # About 1 year
    
    # Wrap the GridFS file as a WSGI file object
    data = wrap_file(request.environ,file,buffer_size=BUFFER_SIZE)

    # Create a Flask response object to respond with the file content
    response = current_app.response_class( # Current_app is exposed by flask.globals as a proxy
        data,
        mimetype=file.content_type,
        direct_passthrough=True ### To bypass some additional checks for the response body
        ### Doc: https://werkzeug.palletsprojects.com/en/2.0.x/wrappers/
    )

    # Config the response
    response.content_length = file.length

    # For determining whether the file content has been updated or not by the browser
    response.last_modified = file.upload_date
    response.set_etag(file.md5)

    # Set the time for cache to be valid
    response.cache_control.max_age = CACHE_KEEP_ALIVE_TIME
    response.cache_control.public = True

    # Make the response conditional, if the browser cache already contains 
    # the latest content, then make the response empty
    response.make_conditional(request)

    # Config the response for the "download" mode
    if download:
        response.headers.set(
            'Content-Disposition', 'attachment', filename=file.filename.encode('utf-8') # Specifies the file will be downloaded as an attachment, set the encoding to utf8 to avoid display issues of Chinese chars
        )
    return response

@file.route('/<id>', methods=['GET'])
def view_file(id):
    '''
    Browse file content in the browser
    '''
    id, _ = path.splitext(id)
    id = BSONObjectIdConverter({}).to_python(id)

    return file_response(id)

@file.route('/<id>/download', methods=['GET'])
def download_file(id):
    '''
    Download file content
    In the browswer, a new window will be opened to
    save the file
    '''

    id, _ = path.splitext(id)

    id = BSONObjectIdConverter({}).to_python(id)

    return file_response(id, download=True)

# @file.route('/<id>', methods=['DELETE'])
@file.route('/<id>', methods=['DELETE'])
def delete_file(id):
    '''
    Delete uploaded file
    '''

    id, _ = path.splitext(id)

    try:
        GridFS(mongo.db).delete(objectid.ObjectId(id))
        # collection = mongo.db.collection 
        # res = collection.delete_one({'_id':objectid.ObjectId(id)})
    except NoFile:
        raise NotFound()

    id = BSONObjectIdConverter({}).to_python(id)

    # mongo.remove('request.files['file'].filename, request.files['file']')

    # Get file extension
    # _, ext = path.splitext(request.files['file'].filename)

    # Generate json response
    # return json_response(id='{}{}'.format(id, ext), is_deleted='Yes')
    # return json_response(id='{}'.format(id), is_deleted='Yes' if res.deleted_count > 0 else 'No', delete_count = res.deleted_count if res else 0)
    return json_response(id='{}'.format(id), is_deleted='Yes')










