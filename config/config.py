import os
import boto3

# env
STAGE = "local" if "STAGE" not in os.environ else os.environ["STAGE"]
API_END_POINT = 'http://localhost' if 'API_END_POINT' not in os.environ else os.environ['API_END_POINT']

# aws settings
AWS_REGION = "ap-southeast-1"

if STAGE != 'local':
    ssm = boto3.client('ssm', AWS_REGION)
    response = ssm.get_parameters(Names=['/ecs/cms/mysql/username'], WithDecryption=True)
    USER_NAME = response['Parameters'][0]['Value']
    response = ssm.get_parameters(Names=['/ecs/cms/mysql/password'], WithDecryption=True)
    PASSWORD = response['Parameters'][0]['Value']

# 3rd party services details
AUTH_SERVICE_URL = API_END_POINT
FOLLOW_SERVICE_URL = API_END_POINT

# data source
SOLR_URL = "http://ip-172-31-16-221.ap-southeast-1.compute.internal:8983/solr"

# worker config
QUEUE_URL = "https://sqs.ap-southeast-1.amazonaws.com/{}/{}-search".format(os.environ["AWS_PROJ_ID"], 'devo' if STAGE == 'local' else STAGE)
POLL_SLEEP_TIME = 10

# 3rd party services
PRATILIPI_SERVICE_URL = "{}/{}".format(os.environ['API_END_POINT'], "pratilipis")
AUTHOR_SERVICE_URL = "{}/{}".format(os.environ['API_END_POINT'], "authors")

# store analysis
REDIS_URL = "devo-ecs.e6ocw5.0001.apse1.cache.amazonaws.com"
REDIS_PORT = 8080
REDIS_DB = 6

# search app config
TOP_SEARCH_LIMIT = 10
TOP_SEARCH_AGE_IN_MIN = 3600

# db access details from parameter store
USER_NAME = 'root'
PASSWORD = 'root'
DB = {'name': 'cms', 'host': '', 'port': 3306, 'user': USER_NAME, 'pass': PASSWORD}

if STAGE in ("gamma", "prod"):
    SOLR_URL = "http://ip-172-31-0-99.ap-southeast-1.compute.internal:8983/solr"
    REDIS_URL = "prod-ecs-001.cpzshl.0001.apse1.cache.amazonaws.com"
    DB['host'] = 'product.cr3p1oy4g8ad.ap-southeast-1.rds.amazonaws.com'
elif STAGE == "devo":
    SOLR_URL = "http://ip-172-31-16-221.ap-southeast-1.compute.internal:8983/solr"
    REDIS_URL = "devo-ecs.e6ocw5.0001.apse1.cache.amazonaws.com"
    DB['host'] = 'ecs-devo-db.ctl0cr5o3mqq.ap-southeast-1.rds.amazonaws.com'
elif STAGE == "local":
    SOLR_URL = "http://localhost:8983/solr"
    REDIS_URL = "localhost"
    REDIS_PORT = 6379
    DB['host'] = 'localhost'
