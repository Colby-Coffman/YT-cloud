#!/usr/bin/env python3

import googleapiclient.discovery as discovery
import googleapiclient.http
import auth
import file
import argparse
import os

VIDEO_FORMAT = "https://www.youtube.com/watch?v={0}"

def arg_flow():
    parser = argparse.ArgumentParser()
    parser.add_argument("-cs", "--chunksize", default=4*1024*1024, type=int)
    parser.add_argument("-f", "--file")
    parser.add_argument("-cc", "--clientcredentials")
    parser.add_argument("-s", "--clientsecret")
    parser.add_argument("-g", "--gui", action="store_true")
    parser.add_argument("-i", "--interactive", action="store_true")
    options = parser.parse_args()
    validate_args(options)
    return options

def validate_args(options):
    if ((options.chunksize < -1) or (options.chunksize > (5 * (10 ** 6)))):
        print("Chunk size passed invalid, defaulting to 4 MiB")
        options.chunksize = 4*1024*1024
    
    if options.file != None:
        head, tail = os.path.split(options.file)
        if head == "":
            options.file = os.path.join(os.getcwd(), options.file)
        file.validate(options.file)
    elif options.interactive:
        options.file = file.get_interactively()
    else:
        raise FileNotFoundError("No file supplied. "
                                    "Pass a file path or enter interactive mode -i")
    
    if options.clientsecret != None:
        head, tail = os.path.split(options.clientsecret)
        if head == "":
            options.clientsecret = os.path.join(os.getcwd(), options.clientsecret)
        file.validate(options.clientsecret)
    elif options.interactive:
        options.clientsecret = file.get_interactively(message="Select Secret",
                                                      filter="*.json")
    else:
        options.clientsecret = file.find_secret()
    auth.CLIENT_SECRETS_FILE = options.clientsecret
    
    if options.clientcredentials != None:
        head, tail = os.path.split(options.clientcredentials)
        if head == "":
            options.clientcredentials = os.path.join(os.getcwd(), options.clientcredentials)
        options.clientcredentials = auth.get_credentials(options.clientcredentials)
    elif options.interactive:
        options.clientcredentials = file.get_interactively(message="Select Credentials",
                                                           filter="*.json")
        options.clientcredentials = auth.get_credentials(options.clientcredentials)
    else:
        thisdir = os.path.dirname(__file__)
        local_credentials = os.path.join(thisdir, "client_credentials.json")
        options.clientcredentials = auth.get_credentials(local_credentials)
        

 
    
if __name__ == "__main__":
    options = arg_flow()
    with discovery.build("youtube", "v3", credentials=options.clientcredentials) as youtube:
        request_body = {
            "snippet": {
                "categoryId": "22",
                "description": "YT-Cloud",
                "title": file.get_title(options.file)
            },
            "status": {
                "privacyStatus": "private"
            }
        }
        request_parts = "snippet,status"
        video = googleapiclient.http.MediaFileUpload(options.file,
                                                    chunksize=options.chunksize, resumable=True,
                                                    mimetype="application/octet-stream")
        print(options.file)
        request = youtube.videos().insert(part=request_parts, body=request_body, media_body=video)
        while True:
            status, response = request.next_chunk()
            if response:
                print("Video uploaded: ", VIDEO_FORMAT.format(response["id"]))
                break