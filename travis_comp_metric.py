import requests
import json
import re
import os
import subprocess
from secrets import *

travis_headers = {"Travis-API-Version": "3", "User-Agent": "API Explorer", "Authorization": "token {0}".format(travis_api_key)}
travis_base_url = "https://api.travis-ci.org"

def get_all_travis_data(owner_and_repo):
    try:
        matchObj = re.match(r'.*\/(.*)', owner_and_repo)
        short_name = matchObj.group(1)
        os.chdir(os.path.expanduser("~/repos"))
        os.chdir("./{0}".format(short_name))

        travis_owner_and_repo = owner_and_repo.replace("/", "%2F")

        r = requests.get(travis_base_url + "/repo/{0}/builds?include=build.commit".format(travis_owner_and_repo), headers=travis_headers)
        response = json.loads(r.text)
        file_dict = {}
        has_next = True

        while(has_next):
            for build in response["builds"]:
                file_dict["commit"] = build["commit"]["sha"]
                if commit_exists(file_dict["commit"]):
                    file_dict = {}
                    has_next = False
                    break
                file_dict["current_state"] = build["state"]
                file_dict["previous_state"] = build["previous_state"]
                file_dict["duration"] = build["duration"]
                save_to_file(file_dict["commit"], file_dict)
            response_has_next = response["@pagination"]["next"]
            has_next = response_has_next and has_next
            if has_next:
                r = requests.get(travis_base_url + response["@pagination"]["next"]["@href"], headers=travis_headers)
                response = json.loads(r.text)
                file_dict = {}
    except:
        return {"success": False}

    return {"success": True}


def commit_exists(commit_hash):
    return os.path.isfile(commit_hash + ".json")

def save_to_file(commit_hash, file_dict):
    if (not os.path.isdir("./travis")):
        os.system("mkdir travis")
    with open("travis/" + commit_hash + ".json", 'w') as file:
        file.write(json.dumps(file_dict))

#get_all_travis_data("saasbook/CS169_Great_Course_Guide")