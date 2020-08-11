import requests
import json

PERMANENT_CACHE_FNAME = "Permanent_Cache.txt"
TEMP_CACHE_FNAME = "Temp_Cache.txt"

def _write_to_file(cache, fName):
    with open(fName, 'w') as outfile:
        outfile.write(json.dumps(cache, indent = 2))

def _read_from_file(fName):
    try:
        with open(fName, 'r') as infile:
            res = infile.read()
            return json.loads(res)
    except:
        return {}

def add_tocache(cache_file, cache_key, cache_value):
    temp_cache = _read_from_file(cache_file)
    temp_cache[cache_key] = cache_value
    _write_to_file(temp_cache, cache_file)

def clear_cache(cache_file = TEMP_CACHE_FNAME):
    _write_to_file({}, cache_file)

def make_cache_key(base_url, params_d, private_keys = ["api_key"] ):
    aplphebetized_keys = sorted(params_d.keys())
    res = []
    for item in aplphebetized_keys:
        if item not in private_keys:
            res.append("{}-{}".format(item, params_d[item]))
    return base_url + "_".join(res)

def get(base_url, params = {}, private_keys_to_ignore = ['api_key'], permanent_cache_file = PERMANENT_CACHE_FNAME, temp_cache_file = TEMP_CACHE_FNAME):
    full_url = requests.requestsURL(base_url, params)
    cache_key = make_cache_key(base_url, params, private_keys_to_ignore)    # generates a cache jey that is stored as a dict item in cache files
                                                                            # def
    # load permanent and page specific cache files
    permanent_cache = _read_from_file(permanent_cache_file)                  # read the contents of the cache
    temp_cache = _read_from_file(permanent_cache_file)                       # def

    if cache_key in temp_cache:
        print("Found in temp cache")
        return requests.Response(temp_cache[cache_key], full_url)
    elif cache_key in permanent_cache:
        print("Found in permanent cache")
        return requests.Response(permanent_cache[cache_key], full_url)
    else:
        print("adding to the cache")
        resp = requests.get(base_url, params)
        add_to_cache(temp_cache_file, cache_key, resp.text)                 # def add_to_cache
        return resp
