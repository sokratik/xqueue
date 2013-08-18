"""
sokratik config for xqueue,, uses postgres and low cost aws settings. no theming is involved here
interfaces with config repo integrated into bitbucket
"""

__author__ = 'vulcan'

from settings import *
import json
from logsettings import get_logger_config
from os.path import expanduser
CONFIG_ROOT = path(expanduser("~")) / "sokratik-infra/json-configs"

# specified as an environment variable.  Typically this is set
# in the service's upstart script and corresponds exactly to the service name.
# Service variants apply config differences via env and auth JSON files,
# the names of which correspond to the variant.
SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', "xqueue")

# when not variant is specified we attempt to load an unvaried
# config set.
CONFIG_PREFIX = ""

if SERVICE_VARIANT:
    CONFIG_PREFIX = SERVICE_VARIANT + "."


with open(CONFIG_ROOT / CONFIG_PREFIX + "env.json") as env_file:
    ENV_TOKENS = json.load(env_file)

XQUEUES = ENV_TOKENS['XQUEUES']
XQUEUE_WORKERS_PER_QUEUE = ENV_TOKENS['XQUEUE_WORKERS_PER_QUEUE']
S3_BUCKET_PREFIX = ENV_TOKENS.get('S3_BUCKET_PREFIX', S3_BUCKET_PREFIX)
LOG_DIR = ENV_TOKENS['LOG_DIR']
local_loglevel = ENV_TOKENS.get('LOCAL_LOGLEVEL', 'INFO')
TIME_ZONE = ENV_TOKENS.get('TIME_ZONE', TIME_ZONE)
LOGGING = get_logger_config(LOG_DIR,
                            logging_env=ENV_TOKENS['LOGGING_ENV'],
                            syslog_addr=(ENV_TOKENS['SYSLOG_SERVER'], 5140),
                            local_loglevel=local_loglevel,
                            debug=True)
RABBIT_HOST = ENV_TOKENS.get('RABBIT_HOST', RABBIT_HOST).encode('ascii')
RABBITMQ_VIRTUAL_HOST = ENV_TOKENS.get('RABBIT_VHOST')


with open(CONFIG_ROOT / CONFIG_PREFIX + "auth.json") as auth_file:
    AUTH_TOKENS = json.load(auth_file)

DATABASES = AUTH_TOKENS['DATABASES']

AWS_ACCESS_KEY_ID = AUTH_TOKENS["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = AUTH_TOKENS["AWS_SECRET_ACCESS_KEY"]

REQUESTS_BASIC_AUTH = AUTH_TOKENS["REQUESTS_BASIC_AUTH"]
RABBITMQ_USER = AUTH_TOKENS.get('RABBITMQ_USER', 'guest').encode('ascii')
RABBITMQ_PASS = AUTH_TOKENS.get('RABBITMQ_PASS', 'guest').encode('ascii')
XQUEUE_USERS = AUTH_TOKENS.get('USERS', None)
SECRET_KEY = AUTH_TOKENS.get("SECRET_KEY")

