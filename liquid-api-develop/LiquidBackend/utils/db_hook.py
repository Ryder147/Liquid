import os
import json

def get_db_credentials():

    MANDATORY_ENV_VARS = [
        "DB_ENGINE", 
        "DB_NAME", 
        "DB_USER", 
        "DB_PASSWORD", 
        "DB_HOST", 
        "DB_PORT"
    ]

    for var in MANDATORY_ENV_VARS:
        if var not in os.environ:
            return get_credentials_from_file()
            
    return {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }

def get_credentials_from_file():
    with open('db_credentials.json') as file:
        return json.load(file)