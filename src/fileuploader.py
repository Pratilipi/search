"""
Pratilipi Search Data Uploader
Currently support search indexes are
- Author
- Pratilipi
"""

import os
import io
import sys
import gzip
import simplejson as json
import csv

PATH = '/home/gauri/Downloads/solr_data'
input_file_name = PATH + '/AUTHOR'
out_file_name = PATH + '/author_solr.json.gz'
author = {}
line_cntr = 0
failed_line_cntr = 0

def readfile(filepath):
    with open(filepath, 'r') as file_obj:
        for line in file_obj:
            yield line.strip()

try:
    with gzip.open(out_file_name, 'wb') as out_file_obj:
        for line in readfile(input_file_name):
            row = json.loads(line.strip())

            try:
                temp = {}
                temp['author_id'] = str(row['AUTHOR_ID'])
                temp['language'] = row['LANGUAGE']
                temp['first_name'] = row['FIRST_NAME']
                temp['last_name'] = row['LAST_NAME']
                temp['first_name_en'] = row['FIRST_NAME_EN']
                temp['last_name_en'] = row['LAST_NAME_EN']
                temp['pen_name'] = row['PEN_NAME']
                temp['pen_name_en'] = row['PEN_NAME_EN']
                temp['summary'] = row['SUMMARY']
            except Exception as err:
                print "Failed while procesing Author line - ", str(err), line
                failed_line_cntr = line_cntr + 1
                continue

            try:
                outLine = json.dumps(temp)
                out_file_obj.write(outLine)
                out_file_obj.write('\n')
            except Exception as err:
                print "Failed while writing to Author output file - ", str(err), line
                failed_line_cntr = line_cntr + 1
                continue

            line_cntr = line_cntr + 1
except Exception as err:
    print "Failed while reading Author data - ", str(err)


print "Author Total: ", line_cntr, " Failed: ", failed_line_cntr


# Pratilipi Data
input_file_name = PATH + '/PRATILIPI'
out_file_name = PATH + '/pratilipi_solr.json.gz'
line_cntr = 0
failed_line_cntr = 0

try:
    with gzip.open(out_file_name, 'wb') as out_file_obj:
        for line in readfile(input_file_name):
            row = json.loads(line.strip())

            try:
                temp = {}
                temp['pratilipi_id'] = row['PRATILIPI_ID']
                temp['author_id'] = row['AUTHOR_ID']
                temp['language'] = row['LANGUAGE']
                temp['title'] = row['TITLE']
                temp['title_en'] = row['TITLE_EN']
                temp['summary'] = row['SUMMARY']
                temp['content_type'] = row['CONTENT_TYPE']
                temp['category'] = row['CATEGORY']
                temp['category_en'] = row['CATEGORY_EN']
            except Exception as err:
                print "Failed while procesing Pratilipi line - ", str(err)
                failed_line_cntr = failed_line_cntr + 1
                continue

            try:
                outLine = json.dumps(temp)
                out_file_obj.write(outLine)
                out_file_obj.write('\n')
            except Exception as err:
                print "Failed while writing to Pratilipi output file - ", str(err), line
                failed_line_cntr = failed_line_cntr + 1
                continue

            line_cntr = line_cntr + 1
except Exception as err:
    print "Failed while reading Pratilipi data - ", str(err)

print "Pratilipi Total: ", line_cntr, " Failed: ", failed_line_cntr

