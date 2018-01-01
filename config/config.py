import os

# env
STAGE = "local" if "STAGE" not in os.environ else os.environ["STAGE"]

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

if STAGE in ("gamma", "prod"):
    SOLR_URL = "http://ip-172-31-0-99.ap-southeast-1.compute.internal:8983/solr"
    REDIS_URL = "prod-ecs-001.cpzshl.0001.apse1.cache.amazonaws.com"
elif STAGE == "devo":
    SOLR_URL = "http://ip-172-31-16-221.ap-southeast-1.compute.internal:8983/solr"
    REDIS_URL = "devo-ecs.e6ocw5.0001.apse1.cache.amazonaws.com"
elif STAGE == "local":
    SOLR_URL = "http://localhost:8983/solr"
    REDIS_URL = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 9
