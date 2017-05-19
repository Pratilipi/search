from commonfns import log_formatter, register_request
import bigquery_ops


def register_search_activity(data):
    """
    add an entry to solr core
    """
    try:
        #prepare url for solr
        url = "{}/{}".format(config_dict['solr_url'], "search_activity/update/json/docs?commit=true")

        print log_formatter(inspect.stack()[0][3], "solr url %s" % url)

        response = requests.post(url, data)
        if response.status_code != 200:
            return False
        if json.loads(response["responseHeader"]["status"]) != 0:
            return False
    except Exception as err:
        print log_formatter(inspect.stack()[0][3], "failed logging search activity")
        return False
    return True


def register_request(log_user_activity, param_dict):
    #insert into solr - trending search
    if param_dict['author_counter'] > 0 or param_dict['pratilipi_counter'] > 0:
        data = {"activity_date": datetime.now().strftime("%Y-%m-%d"),
                "activity_hour": datetime.now().strftime("%H"),
                "platform": param_dict['platform'],
                "lang": param_dict['lang'],
                "keyword": param_dict['text']}
        register_search_activity(data)

    #insert into bigquery - log all user activity
    if not bigquery_ops.stream_data(log_user_activity, param_dict):
        print log_formatter(inspect.stack()[0][3], "failed logging request")
        return False

    return True


def search(config_dict, data):
    """
    Search
    - fetch data from datastore(solr) for authors and pratilipis
    - register request for analysis
    """

    #parse query dict
    userid = data.get('userid', None)
    text = data.get('text', None)
    lang = data.get('lang', None)
    platform = data.get('platform', 'web')
    is_active = data.get('is_active', True)
    limit = data.get('limit', 20)
    offset = data.get('offset', 0)

    if text is None:
        return [400, "Bad Request"]

    try:
        #fetch authors
        #prepare url for solr
        state_filter = "ACTIVE" if is_active else "*"
        lang_filter = '{}'.format(lang) if lang is not None else '*'
        param_dict = {'wt':'json',
                      'fl':'author_id',
                      'sort':'score desc, read_count desc',
                      'rows':limit,
                      'start':offset,
                      'q':'*{}* AND state:{} AND lang:{}'.format(text, state_filter, lang_filter)}
        url = "{}/{}".format(config_dict['solr_url'], "author/select")

        print log_formatter(inspect.stack()[0][3], "solr url %s" % url)

        #prepare author dict
        author = []
        author_count = 0
        response = requests.get(url, params=param_dict)
        if response.status_code == 200:
            data = json.loads(response.text)
            author_count = data['response']['numFound']
            for row in data['response']['docs']:
                author.append(row['author_id'])


        #fetch pratilipis
        #prepare url for solr
        state_filter = "PUBLISHED" if is_active else "*"
        lang_filter = '{}'.format(lang) if lang is not None else '*'
        param_dict = {'wt':'json', 
                      'fl':'pratilipi_id', 
                      'sort':'score desc, read_count desc', 
                      'rows':limit,
                      'start':offset,
                      'q':'*{}* AND state:{} AND lang:{}'.format(text, state_filter, lang_filter)}
        url = "{}/{}".format(config_dict['solr_url'], "pratilipi/select")

        print log_formatter(inspect.stack()[0][3], "solr url %s" % url)

        #prepare pratilipi dict
        pratilipi = []
        pratilipi_count = 0
        response = requests.get(url, params=param_dict)
        if response.status_code == 200:
            data = json.loads(response.text)
            pratilipi_count = data['response']['numFound']
            for row in data['response']['docs']:
                pratilipi.append(row['pratilipi_id'])

        #generate author response
        response = {}
        if author_count > 0:
            response['authors_found'] = author_count
            url = "{}".format(config_dict['author_url'])
            param_dict = {'id':author}
            service_response = requests.get(url, params=param_dict)
            if service_response.status_code == 200:
                response['authors'] = json.loads(service_response.text)
            else:
                print log_formatter(inspect.stack()[0][3], "call failed to author service")

        #generate pratilipi response
        if pratilipi_count > 0:
            response['pratilipis_found'] = pratilipi_count
            url = "{}".format(config_dict['pratilipi_url'])
            param_dict = {'id':pratilipi}
            service_response = requests.get(url, params=param_dict)
            if service_response.status_code == 200:
                response['pratilips'] = json.loads(service_response.text)
            else:
                print log_formatter(inspect.stack()[0][3], "call failed to pratilipi service")

        #if response is empty
        if not bool(response):
            return [204, "No Content"]

        #register request for analysis
        param_dict = (lang, userid, platform, text,
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     author_count, pratilipis_count)
        thr = threading.Thread(target=register_request, args=(config_dict['log_user_activity'], param_dict))
        print log_formatter(inspect.stack()[0][3], "starting thread")
        thr.start()

        #return response
        return [200, "Success", response]
    except Exception as err:
        print log_formatter(inspect.stack()[0][3], "failed while searching - {}".format(str(err)))
        return [500, 'Internal Server Error']


def trending_search(config_dict, data):
    """
    Trending Search
    - fetch data from datastore(solr) for trending search keywords
    """

    #parse query dict
    lang = data.get('lang', 'HINDI')
    platform = data.get('platform', 'web')
    limit = config_dict['trending_limit']
    age = config_dict['trending_age']

    try:
        #fetch search activities
        #prepare url for solr
        lang_filter = '{}'.format(lang) if lang is not None else '*'
        param_dict = {'wt':'json',
                      'fl':'author_id',
                      'sort':'score desc, read_count desc',
                      'rows':limit,
                      'q':'*{}* AND state:{} AND lang:{}'.format(text, state_filter, lang_filter)}
        url = "{}/{}".format(config_dict['solr_url'], "author/select")

        print log_formatter(inspect.stack()[0][3], "solr url %s" % url)

        #generate response
        response = {'trending_keywords': []}
        trending_keywords = []
        response = requests.get(url, params=param_dict)
        if response.status_code == 200:
            data = json.loads(response.text)
            for row in data['response']['docs']:
                response['trending_keywords'].append(row['keyword'])

        #return response
        return [200, "Success", response]
    except Exception as err:
        print log_formatter(inspect.stack()[0][3], "failed while getting trending search - {}".format(str(err)))
        return [500, 'Internal Server Error']

