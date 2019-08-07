import ujson
from algoliasearch import algoliasearch

from config import config
from lib import serviceapis

ALGOLIA_APP_ID = config.ALGOLIA_APP_ID
ALGOLIA_API_KEY = config.ALGOLIA_API_KEY


class Pratilipi:
    def __init__(self, kwargs):
        """init"""

        """algolia connection setup"""
        algolia_client = algoliasearch.Client(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
        algolia_client.search_timeout = (1, 5)
        algolia_client.timeout = (1, 30)
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
        # Currently not adding, as taking care in update as upsert

    def delete(self):
        """delete from algolia"""
        if self.get() is None:
            return

        pdict = {}
        pdict['pratilipi_id'] = self.pratilipi_id
        pdict['deleted'] = True
        pdict['user_id'] = 0
        pratilipis = serviceapis.get_pratilipis_meta(pdict)

        if len(pratilipis) <= 0:
            return

        temp = pratilipis[0]
        language = temp['language'].lower()
        algolia_index = self._algolia.init_index("prod_{}_pratilipi".format(language))
        algolia_index.delete_object(self.pratilipi_id)
        print "------pratilipi deleted - ", self.pratilipi_id

    def update(self):
        print 'updating the algolia pratilipi object'

        pdict = {'pratilipi_id': self.pratilipi_id, 'user_id': 0}
        pratilipis = serviceapis.get_pratilipis(pdict)

        if len(pratilipis) <= 0:
            return

        pratilipi = pratilipis[0]
        if pratilipi.get('language', None) is None:
            return

        self._algolia_index = self._algolia.init_index('prod_{}_pratilipi'.format(pratilipi.get('language').lower()))
        self._algolia_author_index = self._algolia.init_index(
            'prod_{}_author'.format(pratilipi.get('language').lower()))

        if pratilipi['state'] != 'PUBLISHED':
            self._algolia_index.delete_object(self.pratilipi_id)
            return

        category = []
        categoryEn = []
        tags = pratilipi.get('tags', [])

        for tag in tags:
            if tag['name'] is not None:
                category.append(tag['name'])

            if tag['nameEn'] is not None:
                categoryEn.append(tag['nameEn'])

        pdict = {}
        author = {}
        pdict['author_id'] = pratilipi['author']['authorId']
        pdict['user_id'] = 0
        authors = serviceapis.get_authors(pdict)

        if len(authors) > 0 and authors[0].get('language') is not None:
            author = authors[0]

            self._algolia_author_index.partial_update_objects([{
                "objectID": author['authorId'],
                "name": author.get('name', ""),
                "nameEn": author.get('nameEn', ""),
                "penName": author.get('penName', ""),
                "penNameEn": author.get('penNameEn', ""),
                "firstName": author.get('firstName', ""),
                "lastName": author.get("lastName", ""),
                "firstNameEn": author.get("firstNameEn", ""),
                "lastNameEn": author.get("lastNameEn", ""),
                "summary": author.get("summary", ""),
                "contentPublished": author["contentPublished"],
                "totalReadCount": author.get("totalReadCount", 0)}], True)
            print "------author updated - ", author['authorId']

        self._algolia_index.partial_update_objects([{
            "objectID": pratilipi['pratilipiId'],
            "title": pratilipi.get('title', ""),
            "titleEn": pratilipi.get('titleEn', ""),
            "readCount": pratilipi.get('readCount', 0),
            "summary": pratilipi.get('summary', ""),
            "contentType": pratilipi.get('type', ""),
            "category": ",".join(category),
            "categoryEn": ",".join(categoryEn),
            "authorId": author["authorId"],
            "authorName": author.get("firstName", "") + " " + author.get("lastName", ""),
            "authorNameEn": author.get("firstNameEn", "") + " " + author.get("lastNameEn", ""),
            "authorPenName": author.get('penName', ""),
            "authorPenNameEn": author.get('penNameEn', "")}], True)
        print "------pratilipi updated - ", self.pratilipi_id

    def get(self):
        """get from algolia"""
        try:
            algolia_index = self._algolia.init_index("prod_{}_pratilipi".format(self.language))
            record = algolia_index.get_object(self.pratilipi_id)
            return ujson.loads(ujson.dumps(record))
        except Exception as err:
            return None

    def getAlgoliaAuthorObject(self, authorId):
        "get author from algolia "
        try:
            author = self._algolia_author_index.get_object(authorId)
            return author
        except Exception as err:
            print "Error while getting author ", err
            return None
