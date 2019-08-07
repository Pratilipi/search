# coding=utf-8

# setting encoding for app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from config import config
import requests
import simplejson as json


def get_authors(pdict):

	
	print "Get authors from author service"
	url = "{}".format(config.AUTHOR_SERVICE_URL)
	print url
	param_dict = {'id':pdict['author_id']}
	print param_dict
	authors = []

	# Call author service for author data
	service_response = requests.get(url, params=param_dict, headers={"User-Id":str(pdict['user_id'])})
	if service_response.status_code == 200:
		print service_response.text
		authors = json.loads(service_response.text)
	else:
		print "Error while fetching authors"

	return authors
	"""
	authors = []
	author = {}
	author['name'] = "name"
	author['nameEn'] = "nameEn"
	author['firstName'] = "TestPratilipi2"
	author['lastName'] = "pratilipi8888"
	author['penName'] = "Testpratilipi8888"
	author['firstNameEn'] = "TestPratilipiEn"
	author['lastNameEn'] = "pratilipi8888En"
	author['penNameEn'] = "Testpratilipi8888En"
	author['summary'] = "me bht hi umda writer hu yotoyototoot"
	author['contentPublished'] = 1
	author['totalReadCount'] = 1
	author['authorId'] = 6800000000391729
	author['language'] = "HINDI"
	authors.append(author)

	return authors
	"""

def get_authors_meta(pdict):
        print "Get authors meta from author service"
        url = "{}/{}".format(config.AUTHOR_SERVICE_URL,"meta_data")
        print url
        param_dict = {'id':pdict['author_id']}
	if pdict['deleted'] == True:
		param_dict['includeState'] = "DELETED"
        print param_dict
        authors = []

        # Call author service for author data
        service_response = requests.get(url, params=param_dict, headers={"User-Id":str(pdict['user_id'])})
        if service_response.status_code == 200:
                print service_response.text
                authors = json.loads(service_response.text)
        else:
                print "Error while fetching authors"

        return authors

	
def get_pratilipis(pdict):

	url = "{}".format(config.PRATILIPI_SERVICE_URL)
	param_dict = {'id':pdict['pratilipi_id']}

	pratilipis = []

	# Call pratilipi service for pratilipi data
	service_response =  requests.get(url, params=param_dict, headers={"User-Id":str(pdict['user_id'])})
	if service_response.status_code == 200:
		print service_response.text
		pratilipis = json.loads(service_response.text)
	else:
		print "Error while getting pratilipis"

	return pratilipis	

def get_pratilipis_meta(pdict):
	"Get pratilipi meta data from pratilipi service"
	url = "{}/{}".format(config.PRATILIPI_SERVICE_URL,"metadata")
	print url
	param_dict = {'id':pdict['pratilipi_id']}
	if pdict['deleted'] == True:
                param_dict['includeState'] = "DELETED"	
	print param_dict
	pratilipis = []

	#call pratilipi serivce for pratilipi meta data
	service_response = requests.get(url, params=param_dict, headers={"User-Id":str(pdict['user_id'])})
        if service_response.status_code == 200:
                print service_response.text
                pratilipis = json.loads(service_response.text)
        else:
                print "Error while getting pratilipis"

        return pratilipis    

def get_pratilipis_published_after(pdict):

    url = "{}/v2.0/pratilipis".format(config.PRATILIPI_SERVICE_URL)
    param_dict = dict(published_after=pdict['published_after'], limit=pdict['limit'], offset=pdict['offset'],
                      state=pdict['state'])

    pratilipis = []

    # Call pratilipi service for pratilipi data
    service_response = requests.get(url, params=param_dict, headers={"User-Id": str(pdict['user_id'])})
    if service_response.status_code == 200:
    		print service_response.text
        	pratilipis = json.loads(service_response.text)
    else:
        	print "Error while getting pratilipis"

    return pratilipis

