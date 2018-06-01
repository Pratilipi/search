# coding=utf-8

# setting encoding for app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import simplejson as json


def get_authors(config_dict,pdict):

	url = "{}".format(config_dict['author_url'])
	param_dict = {'id':pdict['author_id']}

	authors = []

	# Call author service for author data
	service_response = requests.get(url, params=param_dict, headers={"User-Id":str(pdict['userid'])})
	if service_response.status_code == 200:
		print service_response.text
		authors = json.loads(service_response.text)
	else:
		print "Error while fetching authors"

	return authors
	
	
def get_pratilipis(config_dict,pdict):

	url = "{}".format(config_dict['pratilipi_url'])
	param_dict = {'id':pdict['pratilipi_id']}

	pratilipis = []

	# Call pratilipi service for pratilipi data
	service_response =  requests.get(url, params=param_dict, headers={"User-Id":str(pdict['userid'])})
	if service_response.status_code == 200:
		print service_response.text
		pratilipis = json.loads(service_response.text)
	else:
		print "Error while getting pratilipis"

	return pratilipis	
