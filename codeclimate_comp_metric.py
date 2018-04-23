import requests
import json
import re
import os
import subprocess
from secrets import *

cc_headers = {"Authorization": "Token token=" + codeclimate_api_key , "Accept": "application/vnd.api+json"}



def get_all_codeclimate_data(owner_and_repo):
    matchObj = re.match(r'.*\/(.*)', owner_and_repo)
    short_name = matchObj.group(1)
    os.chdir(os.path.expanduser("~/repos"))
    os.chdir("./{0}".format(short_name))
    # r = requests.get("https://api.codeclimate.com/v1/repos?github_slug={0}".format(owner_and_repo), headers=cc_headers)
    # response = json.loads(r.text)
    # repo_id = response["data"][0]["id"]
    repo_id = "59ee8a344eb04002790006bc"
    r = requests.get("https://api.codeclimate.com/v1/repos/{0}/ref_points?page[size]=100&filter[analyzed]=True&filter[branch]=master".format(repo_id), headers=cc_headers)
    response = json.loads(r.text)
    commit_to_snapshot = {}
    has_next = True
    while (has_next):
        for datapt in response["data"]:
            try:
                print(datapt)
                commit_to_snapshot[datapt["attributes"]["commit_sha"]] = datapt["relationships"]["snapshot"]["data"]["id"]
            except:
                print("ERROR?: ")
                print(datapt)
        has_next = response["links"] != {} and "next" in response["links"]
        if has_next:
            r = requests.get(response["links"]["next"])
            response = json.loads(r.text)
    print(commit_to_snapshot)
    for commit, snapshot in commit_to_snapshot.items():
        file_dict = {}
        r = requests.get("https://api.codeclimate.com/v1/repos/{0}/snapshots/{1}".format(repo_id, snapshot), headers=cc_headers)
        response = json.loads(r.text)
        has_next = True
        print(response)
        while(has_next):
            for file in response["data"]:
                try:
                    file_dict[file["attributes"]["path"]] = file["attributes"]["rating"]
                except:
                    print("ERROR?: ")
                    print(file)
            has_next = response["links"] != {} and "next" in response["links"]
            if has_next:
                r = requests.get(response["links"]["next"])
                response = json.loads(r.text)
        save_to_file(commit, file_dict)

def save_to_file(commit_hash, file_dict):
    if (not os.path.isdir("./codeclimate")):
        os.system("mkdir codeclimate")
    with open("codeclimate/" + commit_hash + ".json", 'w') as file:
        file.write(json.dumps(file_dict))

#get_all_codeclimate_data("saasbook/CS169_Great_Course_Guide")
