import os
import ujson
import time
import boto3
import solr

# setting encoding for app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# config
SOLR_URL = "http://localhost:8983/solr"
STAGE = "local" if "STAGE" not in os.environ else os.environ["STAGE"]
QUEUE_URL = "https://sqs.ap-southeast-1.amazonaws.com/{}/{}-author".format(os.environ["AWS_PROJ_ID"], STAGE)


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
        self.conn = solr.Solr('{}/author'.format(SOLR_URL))
        for name in kwargs:
            setattr(self, name, kwargs[name])
        print "author obj init ", self.__dict__()

    def add(self):
        """add doc"""
        doc = self.__dict__()
        self.conn.add(doc, commit=True)
        print "author added ", doc

    def delete(self):
        """delete doc"""
        self.conn.delete(author_id=self.author_id, commit=True)
        print "author deleted ", self.author_id

    def update(self):
        """update doc"""
        self.add()

class Pratilipi:
    def __init__(self, kwargs):
        """init"""
        self.conn = solr.Solr('{}/pratilipi'.format(SOLR_URL))
        for name in kwargs:
            setattr(self, name, kwargs[name])
        print "pratilipi obj init ", self.__dict__()

    def add(self):
        """add doc"""
        doc = self.__dict__()
        self.conn.add(doc, commit=True)
        print "pratilipi added ", doc

    def delete(self):
        """delete doc"""
        self.conn.delete(pratilipi_id=self.pratilipi_id, commit=True)
        print "pratilipi deleted ", self.pratilipi_id

    def update(self):
        """update doc"""
        self.add()

class SearchQueue:
    def __init__(self):
        """init sqs"""
        setattr(self, 'client', boto3.client('sqs', region_name='ap-southeast-1'))
        setattr(self, 'url', QUEUE_URL)

    def poll(self):
        """poll queue"""
        setattr(self, 'events', [])
        response = self.client.receive_message( QueueUrl = self.url,
                                                AttributeNames = [ 'SentTimestamp' ],
                                                MaxNumberOfMessages = 10,
                                                MessageAttributeNames = [ 'All' ],
                                                VisibilityTimeout = 0,
                                                WaitTimeSeconds = 0 )
        for msg in response['Messages']:
            body = ujson.loads(msg['Body'])
            data = body['Message']
            temp = ujson.loads(data)

            event = Event
            event.type = temp['event']
            event.version = temp['version']
            event.resource_id = temp['meta']['resourceId']
            event.message = {} if 'message' not in temp else temp['message']
            event.rcpthandle = msg['ReceiptHandle']
            self.events.append(event)

    def process_author(self, action, author_id, kwargs):
        kwargs['author_id'] = author_id
        author = Author(kwargs)
        print "encountered author ", action, kwargs
        eval("{}.{}()".format("author", action.lower()))

    def process_pratilipi(self, action, pratilipi_id, kwargs):
        kwargs['pratilipi_id'] = pratilipi_id
        pratilipi = Pratilipi(kwargs)
        print "encountered pratilipi ", action, kwargs
        eval("{}.{}()".format("pratilipi", action.lower()))

    def process(self):
        """process queue"""
        print "processing event"
        events = self.events
        for event in events:
            resource, action = event.type.upper().split('.')

            if event.version != "2.0": continue
            if resource not in ("AUTHOR", "PRATILIPI"): continue
            if action not in ("ADD", "DELETE", "UPDATE"): continue

            if resource == "AUTHOR":
                self.process_author(action, event.resource_id, event.message)
            elif resource == "PRATILIPI":
                self.process_pratilipi(action, event.resource, event.message)
            self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )


print "worker started listening for events...."
while True:
    print "poll queue...."
    event_q = SearchQueue()
    event_q.poll()

    if len(event_q.events) > 0:
        event_q.process()
    print "sleeping now...."
    time.sleep(30)

