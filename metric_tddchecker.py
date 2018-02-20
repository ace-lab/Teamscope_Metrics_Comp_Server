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
    relevant_commits = subprocess.check_output(["git", "log", '--pretty=format:"%H"', "--since=65.days"]).decode("utf-8")
    relevant_commits_list = relevant_commits.split("\n")
    print(relevant_commits_list)
    retVal = {}

    for i in range(len(relevant_commits_list) - 1, 0, -1):
        rollback = relevant_commits_list[i-1].replace('"', '')
        comp_branch = relevant_commits_list[i].replace('"', '')
        diff_results = subprocess.check_output(["diff-cover", "../commits/{0}.xml".format(rollback), "--compare-branch={0}".format(comp_branch)]).decode("utf-8")
        total_match = re.match(r'Total:   (\d+)', diff_results)
        if total_match:
            total = int(total_match.group(0))
        else:
            total = 0
        missing_match = re.match(r'Missing: (\d+)', diff_results)
        if missing_match:
            missing = int(missing.group(0))
        else:
            missing = 0
        inside_dict = {}
        inside_dict.update({"commit_before": comp_branch, "total": total, "missing": missing})
        retVal[rollback] = inside_dict

    os.chdir("..")
    if (not(os.path.isdir("tddresults"))):
        os.system("mkdir tddresults")
    with open("tddresults/result.json", "w") as file:
        file.write(json.dumps(retVal))

#compute_tdd_metric("saasbook/CS169_Great_Course_Guide")
