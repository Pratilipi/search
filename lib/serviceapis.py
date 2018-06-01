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
		author_arr = json.loads(service_response.text)
		if len(author_arr) > 0:
			author = {}
			temp = author_arr[0]
	                author['authorId'] = temp['authorId']
			author['firstName'] = temp['']
                   	author['name'] = temp['fullName'] if 'fullName' in row and row.get('fullName', None) is not None else row['fullNameEn']
                    	author['pageUrl'] = temp['pageUrl'] if 'pageUrl' in row else ''
                    	author['imageUrl'] = temp['coverImageUrl'] if 'coverImageUrl' in row else ''
                    	author['profileImageUrl'] = temp['profileImageUrl'] if 'profileImageUrl' in row else ''
                    	author['followCount'] = temp['followCount'] if 'followCount' in row else 0
                    	author['contentPublished'] = temp['contentPublished'] if 'contentPublished' in row else 0
                    	author['totalReadCount'] = temp['totalReadCount'] if 'totalReadCount' in row else 0
                    	author['following'] = temp['following'] if 'following' in row else False
			authors.append(author)
		else:
			print "No authors afound"		
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
		ptlp_arr = json.loads(service_response.text)
		if len(ptlp_arr) > 0:
			pratilipi = {}
			temp = ptlp_arr[0]
			pratilipi['objectID'] = temp['pratilipiID']
			pratilipi['title'] = temp['title']
			pratilipi['titleEn'] = temp['titleEn']
			pratilipi['readCount'] = temp['readCount']
			pratilipi['summary'] = temp['summary']
			pratilipi['contentType'] = temp['contentType']
			author = temp['author']
			pratilipi['authorName'] = author['fullName']
			pratilipi['authorNameEn'] = author['fullNameEn']
			pratilipi['authorPenName'] = author['fulleName']
			pratilipi['authorPenNameEn'] = author['fullNameEn']
			pratilipi['authorId'] = author['authorId']
			
			category = ''
			categoryEn = ''
			prefix = ''
			for tag in pratilipi['tags']:
				category = prefix+tag['name']
				categoryEn = prefix+tag['nameEn']
				prefix=","
			pratilipi['category'] = category
			pratilipi['categoryEn'] = categoryEn
			pratilipis.append(pratilipi)
		else:
			print "No pratilipis found"
	else:
		print "Error while getting pratilipis"

	return pratilipis	
