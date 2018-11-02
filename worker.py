import os
import ujson
import time
import boto3
#import solr
from config import config
from algoliasearch import algoliasearch
from lib import serviceapis

# setting encoding for app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# config
#SOLR_URL = config.SOLR_URL
SQS_QUEUE_URL = config.SQS_QUEUE_URL
POLL_SLEEP_TIME = config.POLL_SLEEP_TIME
SQS_QUEUE_REGION = config.SQS_QUEUE_REGION
ALGOLIA_APP_ID = config.ALGOLIA_APP_ID
ALGOLIA_API_KEY = config.ALGOLIA_API_KEY 

algolia_client = algoliasearch.Client(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

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
	if self.get() is not None:
		pdict = {}
	        pdict['author_id'] = self.author_id
        	pdict['deleted'] = True
		pdict['user_id'] = 0
		authors = serviceapis.get_authors(pdict) 
		if len(authors) > 0:
			temp = authors[0]
			language = temp['language'].lower()
			algolia_index = self._algolia.init_index("prod_{}_author".format(language))
			#print "deleted author"
			algolia_index.delete_object(self.author_id)

			"""delete author related pratilipis"""
			self.algolia_pratilipi_index = self._algolia.init_index("prod_{}_pratilipi".format(language))
			old_ptlps = self.getAlgoliaPratilipisByAuthorId()
			if len(old_ptlps) > 0:
				for hit in old_ptlps['hits']:
					if int(hit['authorId']) == self.author_id:
						print "pratilipi to delete as author deleted ",self.author_id, hit['objectID']
						self.algolia_pratilipi_index.delete_object(hit['objectID'])
        print "------author deleted - ", self.author_id
    
    def update(self):
        """update doc"""
        new_doc = self.__dict__
        print self
        print new_doc
        """update algolia object"""
        pdict = {}
        pdict['author_id'] = new_doc['author_id']
        pdict['user_id'] = 0
        authors = serviceapis.get_authors(pdict)

        if len(authors) > 0:
            author = authors[0]
            if author.get('language') is not None:
                self._algolia_index = self._algolia.init_index("prod_{}_author".format(author.get('language').lower()))
                self.algolia_pratilipi_index = self._algolia.init_index("prod_{}_pratilipi".format(author.get('language').lower()))
                print "prod_{}_author".format(author.get('language').lower())
                if int(author['contentPublished']) > 0:
                    print "create author", author['authorId']
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
                        "totalReadCount":author.get("totalReadCount",0)	
				    }],True)

                    """Update pratilipis with author info"""
                    old_ptlps = self.getAlgoliaPratilipisByAuthorId()
                    ptlps = []
                    for hit in old_ptlps['hits']:
                        if int(hit['authorId']) == self.author_id:
                            print "pratilipi updated with other info",self.author_id, hit['objectID']
                            self.algolia_pratilipi_index.partial_update_object({
							    "objectID":hit['objectID'],
							    "authorName":author.get("name",""),
							    "authorNameEn":author.get("nameEn",""),
							    "authorPenName":author.get("penName"),
							    "authorPenNameEn":author.get("penNameEn")
						    })
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

class Pratilipi:
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
        attribute['pratilipiid'] = 'pratilipi_id'
        attribute['language'] = 'language'
        attribute['authorid'] = 'author_id'
        attribute['title'] = 'title'
        attribute['titleen'] = 'title_en'
        attribute['summary'] = 'summary'
        attribute['cotenttype'] = 'content_type'
        attribute['category'] = 'category'
        attribute['categoryen'] = 'category_en'
        return attribute[key] if key in attribute else None

    def add(self):
        """add doc"""
	#Currently not adding, as taking care in update as upsert

    def delete(self):

	"""delete from algolia"""
	if self.get() is not None:
		pdict = {}
        	pdict['pratilipi_id'] = self.pratilipi_id
	        pdict['deleted'] = True
        	pdict['user_id'] = 0
		pratilipis = serviceapis.get_pratilipis_meta(pdict)
		if len(pratilipis) > 0:
			temp = pratilipis[0]
	                language = temp['language'].lower()
        		algolia_index = self._algolia.init_index("prod_{}_pratilipi".format(language))
			algolia_index.delete_object(self.pratilipi_id)
	
        print "------pratilipi deleted - ", self.pratilipi_id

    def update(self):
	
	print "updating the algolia pratilipi object"
	pdict = {}
        pdict['pratilipi_id'] = self.pratilipi_id
        pdict['user_id'] = 0
        pratilipis = serviceapis.get_pratilipis(pdict)	
	print "got pratilipi for ", self.pratilipi_id
	if len(pratilipis) > 0:
		pratilipi = pratilipis[0]
		if pratilipi.get('language') is not None:
			self._algolia_index = self._algolia.init_index("prod_{}_pratilipi".format(pratilipi.get('language').lower()))
			self._algolia_author_index = self._algolia.init_index("prod_{}_author".format(pratilipi.get('language').lower()))
			print "prod_{}_pratilipi".format(pratilipi.get('language').lower())

			if pratilipi['state'] == "PUBLISHED":
				print "create/update pratilipi"
		
				category = []
				categoryEn = []
				tags = pratilipi.get("tags",[])	
				for tag in tags:
					if tag["name"] is not None:
						category.append(tag["name"])
					if tag["nameEn"] is not None:
						categoryEn.append(tag["nameEn"])
				
				#print "The tags are ",category, categoryEn
				
				temp_author = pratilipi["author"]
				author = self.getAlgoliaAuthorObject(temp_author["authorId"])
				#print "updating pratilipi with following data", pratilipi, author
				if author is not None:
					self._algolia_index.partial_update_objects([{
						"objectID":pratilipi['pratilipiId'],
						"title":pratilipi.get('title',""),
						"titleEn":pratilipi.get('titleEn',""),
						"readCount":pratilipi.get('readCount',0),
						"summary":pratilipi.get('summary',""),
						"contentType":pratilipi.get('type',""),
						"category": ",".join(category),
						"categoryEn": ",".join(categoryEn),
						"authorId":author["objectID"],		
						"authorName":author.get("firstName","")+" "+author.get("lastName",""),
						"authorNameEn":author.get("firstNameEn","")+" "+author.get("lastNameEn",""),
						"authorPenName":author.get('penName',""),
						"authorPenNameEn":author.get('penNameEn',"")
					}],True)
				else:
					self._algolia_index.partial_update_objects([{
                                                "objectID":pratilipi['pratilipiId'],
                                                "title":pratilipi.get('title',""),
                                                "titleEn":pratilipi.get('titleEn',""),
                                                "readCount":pratilipi.get('readCount',0),
                                                "summary":pratilipi.get('summary',""),
                                                "contentType":pratilipi.get('type',""),
                                                "category": ",".join(category),
                                                "categoryEn": ",".join(categoryEn),
                                                "authorId":temp_author["authorId"],      
                                                "authorName":temp_author.get("name",""),
                                                "authorNameEn":temp_author.get("fullNameEn",""),
                                                "authorPenName":"",
                                                "authorPenNameEn":""
                                        }],True)
			else:
				""" Delete if state is other than published """
				print "Delete if state is not published"
				self._algolia_index.delete_object(self.pratilipi_id)	
	
        print "------pratilipi updated - ", self.pratilipi_id

    def get(self):
	"""get from algolia"""
	try:
		record = self._algolia_index.get_object(self.pratilipi_id)
		return ujson.loads(ujson.dumps(record))
	except Exception as err:
		return None

    def getAlgoliaAuthorObject(self,authorId):
	"get author from algolia "
	try:
        	author = self._algolia_author_index.get_object(authorId)
		return author
	except Exception as err:
        	print "Error while getting author ", err
                return None
		

class SearchQueue:
    def __init__(self):
        """init sqs"""
        setattr(self, 'client', boto3.client('sqs', region_name=SQS_QUEUE_REGION))
        setattr(self, 'url', SQS_QUEUE_URL)

    def poll(self):
        """poll queue"""
        setattr(self, 'events', [])
      	 
	response = self.client.receive_message(QueueUrl=self.url, MaxNumberOfMessages=1,  AttributeNames=[ 'SentTimestamp' ])
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
	
	"""
	event = Event
	event.type = "PRATILIPI.ADD"
	event.version = "v2.0"
	event.resource_id = 63239529976300602
	event.message = {
		"title":"Title",
		"titleEn":"Title english ADD 2",
		"language":"HINDI",
		"pratilipiId":"63239529976300601",
		"authorId":"6800000000409487",
		"contentType":"HINDI"
	}
	event.rcpthandle = "abcdefghijklmnop..."
	self.events.append(event)
		
	event = Event
	event.type = "AUTHOR.DELETE"
	event.version = "v2.0"
	event.resource_id = 6800000000391729
	event.message = {
                "firstName":"firstname updated",
		"lastName":"lastName",
		"firstNameEn":"firstname en",
		"lastNameEn":"lastname en",
		"penName":"pen name",
		"penNameEn":"pen name en",
                "authorId":"6800000000391729",
		"language":"HINDI"
        }
        event.rcpthandle = "abcdefghijklmnop..."
        self.events.append(event)
	"""
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
            resource, action = event.type.upper().split('.')

            if resource not in ("AUTHOR", "PRATILIPI"):
                self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )
                continue

            if action not in ("ADD", "DELETE", "UPDATE"):
                self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )
                continue

            if resource == "AUTHOR":
                self.process_author(action, event.resource_id, event.message)
            elif resource == "PRATILIPI":
                self.process_pratilipi(action, event.resource_id, event.message)
            self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )

print "worker started listening for events...."
while True:
    try:
        print "poll queue...."
        event_q = SearchQueue()
        event_q.poll()
    except Exception as err:
        print "ERROR - sqs polling failed, {}".format(err)

    try:
        if len(event_q.events) > 0:
            event_q.process()
        print "sleeping now...."
        time.sleep(POLL_SLEEP_TIME)
    except Exception as err:
        print "ERROR - event processing failed, {}".format(err)


