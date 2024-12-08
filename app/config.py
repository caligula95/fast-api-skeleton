import os

from dotenv import dotenv_values

config_file = dotenv_values(".env")
config = {
    'ALLOWED_ORIGINS': [
        "http://localhost",
        "https://localhost",
        "http://127.0.0.1",
        "https://127.0.0.1",
        "http://127.0.0.1:3000",
        "https://127.0.0.1:3000",
        "http://localhost:3000",
        "https://localhost:3000",
    ],
    'APP_ENV': 'production'
}

config_keys = [
    'DATABASE_USER',
    'DATABASE_PASSWORD',
    'DATABASE_HOST',
    'DATABASE_NAME',
    'DATABASE_PORT',
    'DATABASE_URL',
    'DEBUG_OUTPUT'
]

if len(config_file) > 0:
    for key in config_keys:
        config[key] = ''
        if key in config_file:
            config[key] = config_file[key]
else:
    for key in config_keys:
        config[key] = os.environ.get(key)
