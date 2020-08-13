import requests
import json
import import_with_request_caching

# function that retrives a list of similar movies from TastDive API
def get_movies_from_tastedive(req_movie):
    base_url = "https://tastedive.com/api/similar"
    query_params = {}
    query_params['q'] = req_movie
    query_params['type'] = 'movies'
    query_params['limit'] = 5
    #resp_obj = requests.get(base_url, query_params)
    resp_obj = import_with_request_caching.get(base_url, query_params, permanent_cache_file="Permanent_Cache.txt")
    print(resp_obj.url) # prints movie url
    py_obj = json.loads(resp_obj.text)
    return py_obj

# function that extracts a list of recommended movies
def extract_movie_titles(py_obj):
    ext_movies = []
    des_dict = py_obj['Similar']['Results']
    for item in des_dict:
        #print(item['Name'])
        ext_movies.append(item['Name'])

    return ext_movies

def get_related_titles(m_lst):
    mv_lst = []
    for item in m_lst:
        mv_lst.append(extract_movie_titles(get_movies_from_tastedive(item)))
    return mv_lst

print(get_related_titles(["shutter island", "21"]))
