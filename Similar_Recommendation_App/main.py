import requests
import json

def get_movies_from_tastedive(req_movie):
    base_url = "https://tastedive.com/api/similar"
    query_params = {}
    query_params['q'] = req_movie
    query_params['type'] = 'movies'
    query_params['limit'] = 20
    resp_obj = requests.get(base_url, query_params)
    print(resp_obj.url) # prints movie url
    py_obj = json.loads(resp_obj.text)
    return py_obj

req_str = get_movies_from_tastedive("cast away")
rec_movies = []
des_dict = req_str['Similar']['Results']
for item in des_dict:
    #print(item['Name'])
    rec_movies.append(item['Name'])

print("Recommended Movies: ")
print(rec_movies)
