# setting encoding for app
import sys

import boto3
import ujson
from algoliasearch import algoliasearch

from config import config
from lib import serviceapis
import logging

from pratilipi import Pratilipi

reload(sys)
sys.setdefaultencoding('utf-8')

# config
SQS_QUEUE_URL = config.SQS_QUEUE_URL
POLL_SLEEP_TIME = config.POLL_SLEEP_TIME
SQS_QUEUE_REGION = config.SQS_QUEUE_REGION
ALGOLIA_APP_ID = config.ALGOLIA_APP_ID
ALGOLIA_API_KEY = config.ALGOLIA_API_KEY 

algolia_client = algoliasearch.Client(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

clog = logging.getLogger('algolia-indexer')
clog.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
clog.addHandler(handler)


class Event:
    def __init__(self):
        """init sqs"""
        setattr(self, 'type', None)
        setattr(self, 'version', None)
        setattr(self, 'resource', None)
        setattr(self, 'resource', None)


class Author:
    def __init__(self, kwargs):
        """init"""
 	"""algolia connection setup"""
	algolia_client = algoliasearch.Client(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
	algolia_client.search_timeout = (1, 5)
	algolia_client.timeout = (1,30)
	self._algolia = algolia_client

        for name in kwargs:
            attribute = self.transformer(name)
            if attribute is None: continue
            value = kwargs[name]
            setattr(self, attribute, value)

    def transformer(self, key):
        key = key.lower().strip()
        attribute = {}
        attribute['authorid'] = 'author_id'
        attribute['language'] = 'language'
        attribute['firstname'] = 'first_name'
        attribute['lastname'] = 'last_name'
        attribute['firstnameen'] = 'first_name_en'
        attribute['lastnameen'] = 'last_name_en'
        attribute['penname'] = 'pen_name'
        attribute['pennameen'] = 'pen_name_en'
        attribute['summary'] = 'summary'
        return attribute[key] if key in attribute else None
        
    def add(self):
        """add doc"""
    	#Currently not adding, as taking care in update as upsert

    def delete(self):
	"""delete from algolia"""
	if self.get() is None:
            return

	pdict = {}
	pdict['author_id'] = self.author_id
        pdict['deleted'] = True
	pdict['user_id'] = 0
	authors = serviceapis.get_authors(pdict)

        if len(authors) <= 0:
            return

	temp = authors[0]
	language = temp['language'].lower()
	algolia_index = self._algolia.init_index(config.ALGOLIA_AUTHOR_INDEX_TEMPLATE.format(language))
	algolia_index.delete_object(self.author_id)

	"""delete author related pratilipis"""
	self.algolia_pratilipi_index = self._algolia.init_index(config.ALGOLIA_PRATILIPI_INDEX_TEMPLATE.format(language))
	old_ptlps = self.getAlgoliaPratilipisByAuthorId()
	if len(old_ptlps) <= 0:
            return

	for hit in old_ptlps['hits']:
            if int(hit['authorId']) != self.author_id:
                continue
            self.algolia_pratilipi_index.delete_object(hit['objectID'])
            print "pratilipi to delete as author deleted ",self.author_id, hit['objectID']
        print "------author deleted - ", self.author_id
    
    def update(self):
        """update doc"""
        new_doc = self.__dict__

        pdict = {}
        pdict['author_id'] = new_doc['author_id']
        pdict['user_id'] = 0
        authors = serviceapis.get_authors(pdict)

        if len(authors) <= 0:
            return

        author = authors[0]
        if author.get('language', None) is None:
            return

        self._algolia_index = self._algolia.init_index(config.ALGOLIA_AUTHOR_INDEX_TEMPLATE.format(author.get('language').lower()))
        self.algolia_pratilipi_index = self._algolia.init_index(config.ALGOLIA_PRATILIPI_INDEX_TEMPLATE.format(author.get('language').lower()))

        if int(author['contentPublished']) <= 0:
            try:
                self.algolia_index.delete_object(author['authorId'])
            except Exception as err:
                pass
            return

        self._algolia_index.partial_update_objects([{
            "objectID":author['authorId'],
            "name":author.get('name',""),
            "nameEn":author.get('nameEn',""),
            "penName":author.get('penName',""),
            "penNameEn":author.get('penNameEn',""),
            "firstName":author.get('firstName',""),
            "lastName":author.get("lastName",""),
            "firstNameEn":author.get("firstNameEn",""),
            "lastNameEn":author.get("lastNameEn",""),
            "summary":author.get("summary",""),
            "contentPublished":author["contentPublished"],
            "totalReadCount":author.get("totalReadCount",0) }], True)
        print "------author updated - ", self.author_id

    def get(self):
	"""get from algolia"""
        try:
            record = self._algolia_index.get_object(self.author_id)
            return ujson.loads(ujson.dumps(record))
	except Exception as err:
            return None

    def getAlgoliaPratilipisByAuthorId(self):
	"get pratilipis from algolia by author_id"
	try:
	    records = self.algolia_pratilipi_index.search(self.author_id,{"attributesToRetrieve":"objectID,authorId"})
	    return ujson.loads(ujson.dumps(records))
	except Exception as err:
	    print err
	    return None
		

class SearchQueue:
    def __init__(self):
        """init sqs"""
        setattr(self, 'client', boto3.client('sqs', region_name=SQS_QUEUE_REGION))
        setattr(self, 'url', SQS_QUEUE_URL)

    def poll(self):
        """poll queue"""
        setattr(self, 'events', [])
      	 
	response = self.client.receive_message(QueueUrl=self.url, MaxNumberOfMessages=5,  AttributeNames=[ 'SentTimestamp' ], VisibilityTimeout=600, WaitTimeSeconds=10)
        if 'Messages' not in response: return
        for msg in response['Messages']:
            # TODO validate request as per schema
            body = ujson.loads(msg['Body'])
            data = body['Message']
            temp = ujson.loads(data)
            temp = ujson.loads(temp) if not isinstance(temp, dict) else temp

            event = Event
            event.type = temp['event']
            event.version = temp['version']
            event.resource_id = temp['meta']['resourceId']
            event.message = {} if 'message' not in temp else temp['message']
            event.rcpthandle = msg['ReceiptHandle']
            self.events.append(event)
	
    def process_author(self, action, author_id, kwargs):
        kwargs['authorId'] = author_id
        author = Author(kwargs)
        print "----encountered author - ", action, kwargs
        eval("{}.{}()".format("author", action.lower()))

    def process_pratilipi(self, action, pratilipi_id, kwargs):
        kwargs['pratilipiId'] = pratilipi_id
        pratilipi = Pratilipi(kwargs)
        print "----encountered pratilipi - ", action, kwargs
        eval("{}.{}()".format("pratilipi", action.lower()))

    def process(self):
        """process queue"""
        print "--processing event"
        events = self.events
        for event in events:
            try:
                self.process_event(event)
            except Exception as err:
                clog.error("event processing failed, {}".format(err))

    def process_event(self, event):
        """process queue"""
        resource, action = event.type.upper().split('.')
        if resource == "AUTHOR":
            clog.info("Processing Author event, {}".format(event.resource_id))
            self.process_author(action, event.resource_id, event.message)
        elif resource == "PRATILIPI":
            clog.info("Processing Pratilipi event, {}".format(event.resource_id))
            self.process_pratilipi(action, event.resource_id, event.message)
        self.client.delete_message(QueueUrl=self.url, ReceiptHandle=event.rcpthandle)


while True:
    try:
        print "poll queue...."
        event_q = SearchQueue()
        event_q.poll()
    except Exception as err:
        clog.error("sqs polling failed, {}".format(err))

    try:
        if len(event_q.events) > 0:
            event_q.process()
    except Exception as err:
        clog.error("event processing failed, {}".format(err))

