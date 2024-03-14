import os


class AuthSettings:
    SECRET_KEY = os.getenv('auth_secret_key')
    ALGORITHM = os.getenv('auth_algorithm')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('auth_access_token_expire_minutes'))


auth_settings = AuthSettings
