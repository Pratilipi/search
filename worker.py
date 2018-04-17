import os
import ujson
import time
import boto3
import solr
from config import config

# setting encoding for app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# config
SOLR_URL = config.SOLR_URL
SQS_QUEUE_URL = config.SQS_QUEUE_URL
POLL_SLEEP_TIME = config.POLL_SLEEP_TIME
SQS_QUEUE_REGION = config.SQS_QUEUE_REGION

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
        self._conn = solr.SolrConnection('{}/author'.format(SOLR_URL))
        for name in kwargs:
            attribute = self.transformer(name)
            if attribute is None: continue
            value = kwargs[name]
            setattr(self, attribute, value)

    def __del__(self):
        self._conn.close()

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
        if self.get() is not None: return

        doc = self.__dict__
        self._conn.add(author_id=doc['author_id'], language=doc.get('language'), first_name=doc.get('first_name',None),
                       last_name=doc.get('last_name', None), pen_name=doc.get('pen_name', None),
                       first_name_en=doc.get('first_name_en', None), last_name_en=doc.get('last_name_en'),
                       pen_name_en=doc.get('pen_name_en', None), summary=doc.get('summary', None))
        self._conn.commit()
        print "author added - ", doc

    def delete(self):
        """delete doc"""
        if self.get() is None: return

        self._conn.delete_query("author_id:{}".format(self.author_id))
        self._conn.commit()
        print "author deleted - ", self.author_id

    def get(self):
        """get doc"""
        dataset = self._conn.query("author_id:{}".format(self.author_id))
        data = None
        for row in dataset:
            data = row
        return data

    def update(self):
        """update doc"""
        old_doc = self.get()

        if old_doc is None:
            self.add()
            return

        new_doc = self.__dict__
        for key in new_doc: old_doc[key] = new_doc[key]
        for key in old_doc: setattr(self, key, old_doc[key])
        self.delete()
        self.add()
        print "author updated - ", old_doc

class Pratilipi:
    def __init__(self, kwargs):
        """init"""
        self._conn = solr.SolrConnection('{}/pratilipi'.format(SOLR_URL))
        for name in kwargs:
            attribute = self.transformer(name)
            if attribute is None: continue
            value = kwargs[name]
            setattr(self, attribute, value)

    def __del__(self):
        self._conn.close()

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
        if self.get() is not None: return

        print "in pratilipi add"
        doc = self.__dict__
        self._conn.add(pratilipi_id=doc['pratilipi_id'], language=doc.get('language', None), author_id=doc.get('author_id',None),
                       title=doc.get('title', None), title_en=doc.get('title_en', None),
                       summary=doc.get('summary', None), content_type=doc.get('content_type'),
                       category=doc.get('category', None), category_en=doc.get('category_en', None))
        self._conn.commit()
        print "pratilipi added - ", doc

    def delete(self):
        """delete doc"""
        if self.get() is None: return
        self._conn.delete_query("pratilipi_id:{}".format(self.pratilipi_id))
        self._conn.commit()
        print "pratilipi deleted - ", self.pratilipi_id

    def get(self):
        """get doc"""
        dataset = self._conn.query("pratilipi_id:{}".format(self.pratilipi_id))
        data = None
        for row in dataset:
            data = row
        return data

    def update(self):
        """update doc"""
        old_doc = self.get()

        if old_doc is None:
            self.add()
            return

        new_doc = self.__dict__
        for key in new_doc: old_doc[key] = new_doc[key]
        for key in old_doc: setattr(self, key, old_doc[key])
        self.delete()
        self.add()
        print "pratilipi updated - ", old_doc

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

            """
            if 'version' not in temp or temp['version'] != "2.0":
                self.client.delete_message( QueueUrl=self.url, ReceiptHandle=msg['ReceiptHandle'] )
                continue
            """

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
        print "encountered author - ", action, kwargs
        eval("{}.{}()".format("author", action.lower()))

    def process_pratilipi(self, action, pratilipi_id, kwargs):
        kwargs['pratilipiId'] = pratilipi_id
        pratilipi = Pratilipi(kwargs)
        print "encountered pratilipi - ", action, kwargs
        eval("{}.{}()".format("pratilipi", action.lower()))

    def process(self):
        """process queue"""
        print "processing event...."
        events = self.events
        for event in events:
            resource, action = event.type.upper().split('.')

            """
            if event.version != "2.0":
                self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )
                continue
            """

            if resource not in ("AUTHOR", "PRATILIPI"):
                self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )
                continue

            if action not in ("ADD", "DELETE", "UPDATE"):
                self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )
                continue

            if resource == "AUTHOR":
                print "processing msg_id: {}".format(event.rcpthandle)
                self.process_author(action, event.resource_id, event.message)
            elif resource == "PRATILIPI":
                print "processing msg_id: {}".format(event.rcpthandle)
                self.process_pratilipi(action, event.resource_id, event.message)
            self.client.delete_message( QueueUrl=self.url, ReceiptHandle=event.rcpthandle )
            print "deleted msg_id: {}".format(event.rcpthandle)

print "worker started listening for events...."
while True:
    try:
        print "poll queue...."
        event_q = SearchQueue()
        event_q.poll()

        if len(event_q.events) > 0:
            event_q.process()
        print "sleeping now...."
        time.sleep(POLL_SLEEP_TIME)
    except Exception as err:
        print "ERROR - sqs polling failed, {}".format(err)
