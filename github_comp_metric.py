import requests
import json
import re
import os
import subprocess
from secrets import *

access_token = gh_api_key


def comp_one_commit(owner_and_repo, commit_hash):
    matchObj = re.match(r'.*\/(.*)', owner_and_repo)
    short_name = matchObj.group(1)
    os.chdir(os.path.expanduser("~/repos"))
    os.chdir("./{0}".format(short_name))
    r = requests.get("http://api.github.com/repos/{0}/commits/{1}?access_token={2}".format(owner_and_repo, commit_hash, access_token))
    request = json.loads(r.text)
    file_dict = {}
    file_dict["author_username"] = request["author"]["login"]
    file_dict["timestamp"] = request["commit"]["author"]["date"]
    file_dict["commit_hash"] = commit_hash
    file_dict["files"] = []
    for file in request["files"]:
        filename = file["filename"]
        inner_dict = {}
        inner_dict["additions"] = file["additions"]
        inner_dict["deletions"] = file["deletions"]
        inner_dict["filename"] = filename

        #Find file type
        if re.match(r'^app\/controllers', filename):
            inner_dict["file_type"] = "controller"
        elif re.match(r'^app\/views', filename):
            inner_dict["file_type"] = "view"
        elif re.match(r'^app\/models', filename):
            inner_dict["file_type"] = "model"
        elif re.match(r'^app\/helpers', filename):
            inner_dict["file_type"] = "helper"
        elif re.match(r'^app\/mailers', filename):
            inner_dict["file_type"] = "mailer"
        elif re.match(r'^config', filename):
            inner_dict["file_type"] = "config"
        elif re.match(r'^coverage', filename):
            inner_dict["file_type"] = "coverage"
        elif re.match(r'^db', filename):
            inner_dict["file_type"] = "db"
        elif re.match(r'^features', filename):
            inner_dict["file_type"] = "cucumber-feature"
        elif re.match(r'^lib', filename):
            inner_dict["file_type"] = "lib"
        elif re.match(r'^spec', filename):
            inner_dict["file_type"] = "rspec-spec"
        elif re.match(r'^app\/views', filename):
            inner_dict["file_type"] = "view"
        elif re.match(r'^README', filename):
            inner_dict["file_type"] = "README"
        else:
            inner_dict["file_type"] = "other"

        if file["status"] != "removed" and inner_dict["file_type"] != "other":
            r = requests.get("http://api.github.com/repos/{0}/contents/{1}?access_token={2}".format(owner_and_repo, filename, access_token))
            file_details = json.loads(r.text)
            try:
                inner_dict["filesize"] = file_details["size"]
            except:
                print(filename)
        else:
            if file["status"] != "removed":
                inner_dict["filesize"] = 0
            else:
                inner_dict["filesize"] = -1

        #Add all to file_dict
        file_dict["files"].append(inner_dict)
    save_to_file(commit_hash, file_dict)


def save_to_file(commit_hash, file_dict):
    if (not os.path.isdir("./github")):
        os.system("mkdir github")
    with open("github/" + commit_hash + ".json", 'w') as file:
        file.write(json.dumps(file_dict))

#Main function to start everything
def github_comp(owner_and_repo):
    matchObj = re.match(r'.*\/(.*)', owner_and_repo)
    short_name = matchObj.group(1)
    os.chdir(os.path.expanduser("~/repos"))
    os.chdir("./{0}/{1}".format(short_name, short_name))
    try:
        os.system("git fetch --all")
        os.system("git reset --hard origin/master")
        #should be --since 1.days
        relevant_commits = subprocess.check_output(["git", "log", '--pretty=format:%H', "--since=109.days"]).decode("utf-8")
        relevant_commits_list = relevant_commits.split("\n")
    except:
        return -1
    os.chdir("..")
    #print(relevant_commits_list)
    try:
        check_gh_commit(owner_and_repo, relevant_commits_list)
        return {"success": True}
    except:
        return {"success": False}


def check_gh_commit(owner_and_repo, commits):
    matchObj = re.match(r'.*\/(.*)', owner_and_repo)
    repo = matchObj.group(1)
    os.chdir(os.path.expanduser("~/repos"))
    if (not os.path.isdir("./{0}".format(repo))):
        os.system("mkdir {0}".format(repo))
    os.chdir("./{0}".format(repo))
    calculate = []
    for commit in commits:
        if (not os.path.exists("github/{0}.json".format(commit))):
            calculate.append(commit)
    for commit in calculate:
        comp_one_commit(owner_and_repo, commit)

# github_comp("adnanhemani/CS169_Great_Course_Guide")