from modules import Json

from os.path import isfile

CONFIG_MODULE = {
  "server": {
    "host": "localhost",
    "port": 8000,
    "api_prefix": "/api",
    "ws_prefix": "/ws",
    "logging": {
      "info-file": "server-info.log",
      "error-file": "server-error.log",
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "image_send_freq": 0.01
  },
  "database": {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "password",
    "database": "dbname",
    "table": "tablename"
  }
}

try:
  if isfile("./backend/config.json"):
    CONFIG_MODULE = Json.load("./backend/config.json")
  else:
    print("config.json not found, using default configuration.")
    Json.pretty_dump("./backend/config.json", CONFIG_MODULE)

except Exception as e:
  print(f"Error loading config.json: {e}")

SERVER_HOST = CONFIG_MODULE["server"]["host"]
SERVER_PORT = CONFIG_MODULE["server"]["port"]
API_PREFIX = CONFIG_MODULE["server"]["api_prefix"]
WS_PREFIX = CONFIG_MODULE["server"]["ws_prefix"]
IMAGE_SEND_FREQ = CONFIG_MODULE["server"]["image_send_freq"]

LOGGING_INFO_FILE = CONFIG_MODULE["server"]["logging"]["info-file"]
LOGGING_ERROR_FILE = CONFIG_MODULE["server"]["logging"]["error-file"] 
LOGGING_FORMAT = CONFIG_MODULE["server"]["logging"]["format"]

DB_HOST = CONFIG_MODULE["database"]["host"]
DB_PORT = CONFIG_MODULE["database"]["port"]
DB_USER = CONFIG_MODULE["database"]["user"]
DB_PASSWORD = CONFIG_MODULE["database"]["password"]
DB_NAME = CONFIG_MODULE["database"]["database"]
DB_TABLE = CONFIG_MODULE["database"]["table"]