import logging
import sys
import time

import redis

from config import config
from lib import serviceapis
from pratilipi import Pratilipi

redis_config = {'redis_url': config.REDIS_URL,
               'redis_port': config.REDIS_PORT,
               'redis_db': config.REDIS_DB, }

clog = logging.getLogger('algolia-re-indexer')
clog.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
clog.addHandler(handler)


class ReIndexer:

    def __init__(self):
        self.updated_pratilipis_count = 0
        self.re_indexed_pratilipis_count = 0

    def resume_indexing(self):
        checkpoint = IndexCheckpoint()
        last_indexed_time = checkpoint.get()
        if last_indexed_time is None:
            clog.error("Re-indexing failed. No last indexed time present in redis for resuming")
            return
        limit = 20
        offset = 0
        state = 'PUBLISHED'
        while True:
            try:
                pdict = dict(published_after=last_indexed_time, limit=limit, offset=offset, state=state, user_id=0)
                pratilipis = serviceapis.get_pratilipis_published_after(pdict)
                if len(pratilipis) <= 0:
                    checkpoint.force_save()
                    return
                for pratilipi in pratilipis['data']:
                    self.check_and_index(pratilipi)
                    checkpoint.save(pratilipi['publishedAt'])
                offset = offset + len(pratilipis)
                self.updated_pratilipis_count = offset
            except Exception as err:
                clog.error("Re-indexing failed, {}".format(err))
            time.sleep(5)

    def check_and_index(self, pratilipi):
        kwargs = {'pratilipiId': pratilipi['pratilipiId'], 'language': pratilipi['language']}
        pratilipi = Pratilipi(kwargs)
        if pratilipi.get() is not None:
            return
        clog.info("Re-indexing Pratilipi Id : {}".format(pratilipi.pratilipi_id))
        self.re_indexed_pratilipis_count = self.re_indexed_pratilipis_count + 1
        pratilipi.update()

    def print_indexing_stats(self):
        print "Indexing stats : Total Pratilipis Updated : {}, Re-indexed Pratilipis : {}".format(self.updated_pratilipis_count, self.re_indexed_pratilipis_count)


class IndexCheckpoint:

    def __init__(self):
        redis_client = redis.StrictRedis(redis_config['redis_url'], redis_config['redis_port'], redis_config['redis_db'])
        self.redis_client = redis_client
        self.previous_indexed_time = 0

    def get(self):
        last_indexed_time = int(self.redis_client.get("last_indexed_time"))
        self.previous_indexed_time = last_indexed_time
        return last_indexed_time

    def save(self, last_indexed_time):
        if self.previous_indexed_time == last_indexed_time:
            return
        self.previous_indexed_time = last_indexed_time
        self.force_save()

    def force_save(self):
        self.redis_client.set("last_indexed_time", self.previous_indexed_time)


re_indexer = ReIndexer()
re_indexer.resume_indexing()
re_indexer.print_indexing_stats()

