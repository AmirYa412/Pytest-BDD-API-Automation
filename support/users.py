"""Load environment variables from .env file and define user credentials for different environments."""


import os
from dotenv import load_dotenv

load_dotenv()

PRODUCTION_USERS = {
    "Emily": {
        "username" : "emilys",
        "password" : os.getenv('PROD_EMILY_PASSWORD', None)
    },
    "michael": {
        "username": "michaelw",
        "password": os.getenv('PROD_MICHAEL_PASSWORD', None)
    },
    "Sophia": {
        "username": "sophiab",
        "password": os.getenv('PROD_SOPHIA_PASSWORD', None)
    }
}


CI_USERS = {
    "Emily": {
        "username" : "emilys",
        "password" : os.getenv('CI_EMILY_PASSWORD', None)
    },
    "michael": {
        "username": "michaelw",
        "password": os.getenv('CI_MICHAEL_PASSWORD', None)
    },
    "Sophia": {
        "username": "sophiab",
        "password": os.getenv('CI_SOPHIA_PASSWORD', None)
    }
}

