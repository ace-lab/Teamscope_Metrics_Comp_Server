import subprocess
import json
import os
import re
import subprocess
import sys
#Hope that setup is ok

def compute_tdd_metric(repo):
    os.chdir(os.path.expanduser("~/repos"))
    matchObj = re.match(r'.*\/(.*)', repo)
    short_name = matchObj.group(1)
    os.chdir("./{0}/{1}".format(short_name, short_name))
    os.system("git fetch --all")
    os.system("git reset --hard origin/master")
    relevant_commits = subprocess.check_output(["git", "log", '--pretty=format:"%H"', "--since='2017-08-01T00:00:00-07:00'"]).decode("utf-8")
    relevant_commits_list = relevant_commits.split("\n")
    #print(relevant_commits_list)
    retVal = {}

    for i in relevant_commits_list[::-1]:
        rollback = i.replace('"', '')
        os.system("git reset --hard {0}".format(rollback))
        parent_results = subprocess.check_output(["git", "log", "--pretty=%P", "-n", "1"]).decode("utf-8")
        parent_commits_list = parent_results.split(" ")
        commit_timestamp = subprocess.check_output(["git", "log", "--pretty=%at", "-1"]).decode("utf-8")
        #print(commit_timestamp)
        retVal[rollback] = [int(commit_timestamp)]
        for i in parent_commits_list:
            inside_dict = {}
            comp_branch = i.replace("\n", "")
            if not os.path.exists("../commits/{0}.xml".format(i)):
                inside_dict.update({"commit_before": comp_branch, "total": -1, "missing": -1, "error": "commit file does not exist"})
            else:
                diff_results = subprocess.check_output(["diff-cover", "../commits/{0}.xml".format(rollback), "--compare-branch={0}".format(comp_branch)]).decode("utf-8")
                total_match = re.search(r'Total:(?:\s*)(\d+)', diff_results)
                if total_match:
                    total = int(str(total_match.group(1)))
                else:
                    total = 0
                missing_match = re.search(r'Missing:(?:\s*)(\d+)', diff_results)
                if missing_match:
                    missing = int(str(missing_match.group(1)))
                else:
                    missing = 0
                inside_dict.update({"commit_before": comp_branch, "total": total, "missing": missing})
            retVal[rollback].append(inside_dict)

    os.chdir("..")
    if (not(os.path.isdir("tddresults"))):
        os.system("mkdir tddresults")
    with open("tddresults/result.json", "w") as file:
        file.write(json.dumps(retVal))

compute_tdd_metric("adnanhemani/slc-app")
