import os

def get_stripe_api_key():
    if "STRIPE_API_KEY" not in os.environ:
            return get_key_from_file()
    else:
        return os.getenv("STRIPE_API_KEY")

def get_key_from_file():
    with open('stripe_api_key.txt') as file:
        return file.readline()