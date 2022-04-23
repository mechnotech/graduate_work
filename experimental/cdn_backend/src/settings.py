import os

LINK_EXPIRES_HOURS = int(os.getenv('LINK_EXPIRES_HOURS', 2))
SALT = os.getenv('SALT', '8784dg4rgw44fe73sdf7r72s7')
SECRET_KEY = os.getenv('SECRET_KEY', 'eoni2q_dfgdf55p136e&2wy_dfgdddgx0')
SWAGGER = {'title': 'OA3 Callbacks', 'openapi': '3.0.2', 'specs_route': '/swagger/'}
